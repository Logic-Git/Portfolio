"""
Rubric generation module for Resume Screener.

Handles the generation and modification of scoring rubrics using the Gemini 2.0 Flash API.
"""

import json
import logging
import time
from typing import List, Dict, Any, Optional
import requests
from ratelimit import limits, sleep_and_retry
from google import genai

from config import GEMINI_API_KEY

# Configure logger
logger = logging.getLogger(__name__)

# Initialize Gemini client
if GEMINI_API_KEY:
    genai_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    genai_client = None
    logger.warning(
        "GEMINI_API_KEY is not set, Gemini functionality will be unavailable"
    )


@sleep_and_retry
@limits(calls=10, period=60)
def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Call the Gemini 2.0 Flash API with rate limiting.

    Args:
        prompt: The prompt text to send to Gemini

    Returns:
        str: The response text or None if the call failed
    """
    if not genai_client:
        logger.error("Gemini client is not initialized")
        return None

    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )

        return response.text

    except Exception as e:
        logger.exception(f"Error calling Gemini API: {str(e)}")
        return None


def generate_initial_rubric(job_description: str) -> List[Dict[str, Any]]:
    """
    Generate an initial scoring rubric based on the job description.

    Args:
        job_description: The job description text

    Returns:
        List[Dict]: A list of criteria with their maximum point values
    """
    logger.info("Generating initial rubric with Gemini...")

    prompt = f"""
Based on the following job description, generate a detailed scoring rubric out of 100 points for evaluating resumes.
List each criterion with a maximum point value. The sum of all maximum points should be exactly 100.

Job Description:
{job_description}

Format your response strictly as a JSON array of objects with 'criterion' and 'max_points' keys. Example:
[
  {{"criterion": "Education", "max_points": 20}},
  {{"criterion": "Relevant Experience", "max_points": 30}},
  ...
]
"""

    try:
        response = call_gemini_api(prompt)
        if not response:
            logger.error("Failed to generate rubric from Gemini")
            return default_rubric()

        # Extract JSON from response
        response = response.strip()
        json_start = response.find("[")
        json_end = response.rfind("]") + 1

        if json_start == -1 or json_end == 0:
            logger.error("Could not extract valid JSON from Gemini response")
            return default_rubric()

        json_str = response[json_start:json_end]

        # Parse JSON
        rubric = json.loads(json_str)

        # Validate rubric
        total_points = sum(item.get("max_points", 0) for item in rubric)

        if not rubric or total_points != 100:
            logger.warning(f"Generated rubric has invalid total points: {total_points}")
            return normalize_rubric(rubric)

        logger.info(f"Successfully generated rubric with {len(rubric)} criteria")
        return rubric

    except Exception as e:
        logger.exception(f"Error generating rubric: {str(e)}")
        return default_rubric()


def modify_rubric(
    current_rubric: List[Dict[str, Any]], modifications: str, job_description: str
) -> List[Dict[str, Any]]:
    """
    Modify the current rubric based on user's natural language instructions.

    Args:
        current_rubric: The current rubric
        modifications: Natural language description of modifications
        job_description: Original job description for context

    Returns:
        List[Dict]: The modified rubric
    """
    logger.info(f"Modifying rubric based on user input: {modifications}")

    # Convert current rubric to JSON string
    current_rubric_json = json.dumps(current_rubric, indent=2)

    prompt = f"""
You are modifying a resume scoring rubric. The current rubric is:

{current_rubric_json}

The job description is:
{job_description}

The user wants to make these modifications:
{modifications}

Please generate a new rubric that incorporates these changes while ensuring:
1. The total points still sum to exactly 100
2. The format is maintained as a list of criteria with max_points
3. The weights are appropriately balanced

Format your response strictly as a JSON array of objects with 'criterion' and 'max_points' keys. Example:
[
  {{"criterion": "Education", "max_points": 20}},
  {{"criterion": "Relevant Experience", "max_points": 30}},
  ...
]
"""

    try:
        response = call_gemini_api(prompt)
        if not response:
            logger.error("Failed to modify rubric with Gemini")
            return current_rubric

        # Extract JSON from response
        response = response.strip()
        json_start = response.find("[")
        json_end = response.rfind("]") + 1

        if json_start == -1 or json_end == 0:
            logger.error(
                "Could not extract valid JSON from Gemini response for modified rubric"
            )
            return current_rubric

        json_str = response[json_start:json_end]

        # Parse JSON
        modified_rubric = json.loads(json_str)

        # Validate modified rubric
        total_points = sum(item.get("max_points", 0) for item in modified_rubric)

        if not modified_rubric or total_points != 100:
            logger.warning(f"Modified rubric has invalid total points: {total_points}")
            return normalize_rubric(modified_rubric)

        logger.info(
            f"Successfully modified rubric with {len(modified_rubric)} criteria"
        )
        return modified_rubric

    except Exception as e:
        logger.exception(f"Error modifying rubric: {str(e)}")
        return current_rubric


def normalize_rubric(rubric: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize a rubric to ensure it sums to 100 points.

    Args:
        rubric: The rubric to normalize

    Returns:
        List[Dict]: The normalized rubric
    """
    if not rubric:
        return default_rubric()

    total = sum(item.get("max_points", 0) for item in rubric)
    if total == 0:
        return default_rubric()

    normalized = []
    running_total = 0

    # Normalize all but the last item
    for i, item in enumerate(rubric[:-1]):
        normalized_points = round((item.get("max_points", 0) / total) * 100)
        if normalized_points < 1:
            normalized_points = 1

        running_total += normalized_points
        normalized.append(
            {
                "criterion": item.get("criterion", f"Criterion {i + 1}"),
                "max_points": normalized_points,
            }
        )

    # Make sure the last item makes the total exactly 100
    last_points = 100 - running_total
    if last_points < 1:
        # Adjust previous item to make room for at least 1 point
        normalized[-1]["max_points"] -= 1 - last_points
        last_points = 1

    normalized.append(
        {
            "criterion": rubric[-1].get("criterion", f"Criterion {len(rubric)}"),
            "max_points": last_points,
        }
    )

    return normalized


def default_rubric() -> List[Dict[str, Any]]:
    """
    Return a default resume scoring rubric when generation fails.

    Returns:
        List[Dict]: A default scoring rubric
    """
    return [
        {"criterion": "Education", "max_points": 20},
        {"criterion": "Relevant Experience", "max_points": 30},
        {"criterion": "Skills", "max_points": 25},
        {"criterion": "Projects/Portfolio", "max_points": 15},
        {"criterion": "Resume Quality & Formatting", "max_points": 10},
    ]
