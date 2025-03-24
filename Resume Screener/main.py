#!/usr/bin/env python3
"""
Resume Screener - Main Module

This script provides a CLI for screening resumes against a job description
using Gemini and Deepseek APIs to evaluate candidates.
"""

import os
import sys
import logging
import time
from pathlib import Path

from file_handlers import (
    validate_job_description_path,
    extract_job_description_text,
    get_resume_files,
    extract_resume_text,
)
from rubric_generation import generate_initial_rubric, modify_rubric
from resume_scoring import score_resume, extract_pros_cons
from excel_handler import initialize_results_file, save_result_to_excel
from config import setup_logging, API_RATE_LIMIT

# Initialize logger
logger = logging.getLogger(__name__)


def get_user_input():
    """Get and validate user input for job description and resumes directory."""

    print("\n===== Resume Screener =====")
    print("This tool evaluates resumes against a job description using AI.\n")

    # Get job description file path
    while True:
        jd_path = input("Enter path to job description file (.txt or .docx): ").strip()
        if not jd_path:
            print("Job description file is required. Please provide a valid path.")
            continue

        if validate_job_description_path(jd_path):
            break
        else:
            print("Invalid job description file. Please provide a .txt or .docx file.")

    # Get resumes directory path
    resumes_dir = input(
        "Enter directory containing resumes (.docx and .pdf) [default: current directory]: "
    ).strip()
    if not resumes_dir:
        resumes_dir = os.getcwd()
        print(f"Using current directory: {resumes_dir}")

    if not os.path.isdir(resumes_dir):
        print(f"Directory '{resumes_dir}' does not exist.")
        sys.exit(1)

    return jd_path, resumes_dir


def main():
    """Main function to orchestrate the resume screening process."""

    # Set up logging
    setup_logging()
    logger.info("Resume Screener started")

    try:
        # Get user input
        jd_path, resumes_dir = get_user_input()
        logger.info(f"Job description: {jd_path}")
        logger.info(f"Resumes directory: {resumes_dir}")

        # Extract job description text
        job_description = extract_job_description_text(jd_path)
        if not job_description:
            logger.error("Failed to extract text from job description")
            print("Error: Could not extract text from job description file.")
            sys.exit(1)

        logger.info("Successfully extracted job description text")

        # Generate rubric using Gemini
        rubric = generate_initial_rubric(job_description)

        # Allow user to modify the rubric
        while True:
            print("\n===== Generated Scoring Rubric =====")
            for item in rubric:
                print(f"{item['criterion']}: {item['max_points']} points")

            confirm = input("\nIs this rubric acceptable? (yes/no): ").strip().lower()
            if confirm == "yes":
                logger.info("User confirmed rubric")
                break

            modifications = input("Please describe your modifications: ").strip()
            rubric = modify_rubric(rubric, modifications, job_description)
            logger.info("User modified rubric")
            logger.info("Rubric after modification: %s", rubric)

        # Initialize results file
        results_file = os.path.join(os.getcwd(), "resume_screening_results.xlsx")
        initialize_results_file(results_file)

        # Get resume files
        resume_files = get_resume_files(resumes_dir)
        logger.info(f"Found {len(resume_files)} resumes to process")

        if not resume_files:
            print("No resume files found. Supported formats are .docx and .pdf")
            logger.warning("No resume files found")
            sys.exit(0)

        print(f"\nFound {len(resume_files)} resumes to evaluate.")

        # Process each resume
        for idx, resume_path in enumerate(resume_files, 1):
            print(
                f"\nProcessing resume {idx}/{len(resume_files)}: {os.path.basename(resume_path)}"
            )
            logger.info(f"Processing resume: {resume_path}")

            try:
                # Extract resume text
                resume_text = extract_resume_text(resume_path)
                if not resume_text:
                    logger.error(f"Failed to extract text from resume: {resume_path}")
                    print(
                        f"Error: Could not extract text from {os.path.basename(resume_path)}"
                    )
                    continue

                # Score resume using Gemini and Deepseek
                gemini_score, deepseek_score = score_resume(
                    resume_text, job_description, rubric
                )

                # Calculate average score
                if gemini_score is not None and deepseek_score is not None:
                    avg_score = (gemini_score + deepseek_score) / 2
                elif gemini_score is not None:
                    avg_score = gemini_score
                    logger.warning(f"Using only Gemini score for {resume_path}")
                elif deepseek_score is not None:
                    avg_score = deepseek_score
                    logger.warning(f"Using only Deepseek score for {resume_path}")
                else:
                    logger.error(f"Failed to score resume: {resume_path}")
                    print(f"Error: Could not score {os.path.basename(resume_path)}")
                    continue

                # Extract pros and cons
                pros, cons = extract_pros_cons(resume_text, job_description, rubric)

                # Save results to Excel incrementally
                save_result_to_excel(
                    results_file, os.path.basename(resume_path), avg_score, pros, cons
                )

                print(f"Score: {avg_score:.2f}/100")

            except Exception as e:
                logger.exception(f"Error processing resume {resume_path}: {str(e)}")
                print(f"Error processing {os.path.basename(resume_path)}: {str(e)}")
                continue

            # Respect rate limiting
            if idx < len(resume_files):
                print(f"Pausing briefly to respect API rate limits...")
                time.sleep(API_RATE_LIMIT)

        print(f"\nResume screening completed! Results saved to: {results_file}")
        logger.info("Resume Screener completed successfully")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        logger.info("Operation cancelled by user")
        sys.exit(0)

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        logger.exception(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
