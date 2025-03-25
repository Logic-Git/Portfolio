"""
Resume scoring module for Resume Screener.

Handles scoring resumes using Gemini 2.0 Flash and DeepSeek (via OpenRouter) APIs based on a provided rubric.
"""

import logging
import json
import time
from typing import List, Dict, Any, Tuple, Optional
import requests
from ratelimit import limits, sleep_and_retry
from google import genai
import openai

from config import GEMINI_API_KEY, OPENROUTER_API_KEY

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

# Initialize OpenAI client with OpenRouter base URL for DeepSeek
if OPENROUTER_API_KEY:
    openai_client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
    )
else:
    openai_client = None
    logger.warning(
        "OPENROUTER_API_KEY is not set, DeepSeek functionality will be unavailable"
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


@sleep_and_retry
@limits(calls=10, period=60)
def call_deepseek_api(prompt: str) -> Optional[str]:
    """
    Call the DeepSeek API via OpenRouter with rate limiting.

    Args:
        prompt: The prompt text to send to DeepSeek

    Returns:
        str: The response text or None if the call failed
    """
    if not openai_client:
        logger.error("OpenRouter client for DeepSeek is not initialized")
        return None

    try:
        response = openai_client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful resume evaluation assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2048,
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.exception(f"Error calling DeepSeek API via OpenRouter: {str(e)}")
        return None


def score_resume(
    resume_text: str, job_description: str, rubric: List[Dict[str, Any]]
) -> Tuple[Optional[float], Optional[float]]:
    """
    Score a resume using both Gemini and DeepSeek APIs.

    Args:
        resume_text: The extracted resume text
        job_description: The job description text
        rubric: The scoring rubric

    Returns:
        Tuple[float, float]: Gemini score and DeepSeek score (0-100)
    """
    # Convert rubric to a string format for prompts
    rubric_text = "\n".join(
        [f"- {item['criterion']}: {item['max_points']} points" for item in rubric]
    )

    # Format prompt for scoring
    prompt = f"""
You are an expert resume evaluator. Your task is to score a resume against a rubric given below.

SCORING RUBRIC (out of 100 points):
{rubric_text}

RESUME:
{resume_text}

Instructions:
1. Carefully analyze the resume against each criterion in the rubric.
2. Provide a detailed evaluation with specific scores for each criterion and a final total score.
3. Do not simply award full points for a criterion just because it is mentioned in the resume. Instead, critically evaluate the resume to determine an appropriate score for each criterion.
   - For example, suppose the criterion is "Python":
     ```Then if a person mentions python in their skills section but has no relevant experience or projects mentioned in the resume that use python (neither do any of the experiences or project explicitly mention python nor can you logically infer from the projects that they might have involved programming in python),
then the person gets 0 score for this criterion because simply mentioning it in the skills section is worth nothing.
On the other hand, if the person has vast software engineering projects that they describe in their CV and explicitly mention that they used python for the project or you can logically infer from what the projects are about that python might have been used and they have mentioned python in their skills section at the same time, then it is safe to assume that they have worked a lot in python and you can give them a high score in this criterion.
On the other hand, if there is another person who just has one small project in python then they do not get a 0 but they get a low score in this criterion.```
4. Format your response as a JSON object with the following structure:
   - A "breakdown" object containing scores for each criterion.
   - A "total_score" field with the sum of all individual scores.
   
Example response format:
{{"breakdown": {{"Education": 15,
    "Relevant Experience": 25,
    ...
  }},
  "total_score": 85
}}

5. Ensure that the total score is exactly the sum of all individual scores and does not exceed 100.
"""

    # Get Gemini score
    gemini_score = None
    try:
        gemini_response = call_gemini_api(prompt)
        if gemini_response:
            gemini_score = extract_score_from_response(gemini_response)
            logger.info(f"Gemini scored resume: {gemini_score}")
        else:
            logger.warning("Failed to get Gemini score")
    except Exception as e:
        logger.exception(f"Error getting Gemini score: {str(e)}")

    # Get DeepSeek score
    deepseek_score = None
    try:
        deepseek_response = call_deepseek_api(prompt)
        if deepseek_response:
            deepseek_score = extract_score_from_response(deepseek_response)
            logger.info(f"DeepSeek scored resume: {deepseek_score}")
        else:
            logger.warning("Failed to get DeepSeek score")
    except Exception as e:
        logger.exception(f"Error getting DeepSeek score: {str(e)}")

    return gemini_score, deepseek_score


def extract_score_from_response(response: str) -> Optional[float]:
    """
    Extract score from API response.

    Args:
        response: The API response text

    Returns:
        float: The extracted score or None if parsing failed
    """
    try:
        # Try to find and extract JSON from the response
        response = response.strip()
        json_start = response.find("{")
        json_end = response.rfind("}") + 1

        if json_start == -1 or json_end == 0:
            logger.warning("Could not find JSON in the response")
            # Try to extract a numeric score from the text
            import re

            score_match = re.search(r'total_score["\s:]+(\d+(\.\d+)?)', response)
            if score_match:
                return float(score_match.group(1))
            else:
                logger.error("Could not extract score from response")
                return None

        json_str = response[json_start:json_end]

        # Parse JSON
        result = json.loads(json_str)

        # Get total score
        if "total_score" in result:
            return float(result["total_score"])

        # If total_score is not at the top level, try to calculate from breakdown
        elif "breakdown" in result:
            total = sum(float(score) for score in result["breakdown"].values())
            return total

        else:
            logger.warning("JSON response missing expected fields")
            return None

    except Exception as e:
        logger.exception(f"Error extracting score: {str(e)}")
        return None


def extract_pros_cons(
    resume_text: str, job_description: str, rubric: List[Dict[str, Any]]
) -> Tuple[str, str]:
    """
    Extract pros and cons from a resume comparison with a job description.

    Args:
        resume_text: The extracted resume text
        job_description: The job description text
        rubric: The scoring rubric

    Returns:
        Tuple[str, str]: Pros and cons
    """
    # Convert rubric to a string format for prompts
    rubric_text = "\n".join(
        [f"- {item['criterion']}: {item['max_points']} points" for item in rubric]
    )

    # Format prompt for pros
    pros_prompt = f"""
You are an expert resume evaluator. Analyze this resume against the job description and identify the top 3-5 strengths or pros of this candidate.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

RUBRIC CRITERIA:
{rubric_text}

List only the pros/strengths of this candidate relative to the job requirements, focusing on the most impressive qualifications. Be specific and concise.
Format your response as a bulleted list without any introduction or conclusion.
"""

    # Format prompt for cons
    cons_prompt = f"""
You are an expert resume evaluator. Analyze this resume against the job description and identify the top 3-5 weaknesses, gaps, or areas for improvement.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

RUBRIC CRITERIA:
{rubric_text}

List only the cons/weaknesses/gaps of this candidate relative to the job requirements. Be specific, constructive, and concise.
Format your response as a bulleted list without any introduction or conclusion.
"""

    # Get pros
    pros = "- No strengths could be identified"
    try:
        pros_response = call_gemini_api(pros_prompt)
        if pros_response:
            pros = pros_response.strip()
            logger.info("Successfully extracted pros")
    except Exception as e:
        logger.exception(f"Error extracting pros: {str(e)}")

    # Get cons
    cons = "- No areas for improvement could be identified"
    try:
        cons_response = call_gemini_api(cons_prompt)
        if cons_response:
            cons = cons_response.strip()
            logger.info("Successfully extracted cons")
    except Exception as e:
        logger.exception(f"Error extracting cons: {str(e)}")

    return pros, cons
