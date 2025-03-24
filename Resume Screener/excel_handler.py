"""
Excel handler module for Resume Screener.

Handles creating, reading, and updating Excel files with resume screening results.
"""

import os
import logging
import pandas as pd
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)


def initialize_results_file(file_path: str) -> None:
    """
    Initialize the Excel results file if it doesn't exist.

    Args:
        file_path: Path to the Excel file
    """
    if os.path.exists(file_path):
        logger.info(f"Results file already exists: {file_path}")
        return

    # Create a new DataFrame with the required columns
    df = pd.DataFrame(columns=["File Name", "Average Score", "Pros", "Cons"])

    try:
        # Save the empty DataFrame to create the file
        df.to_excel(file_path, index=False, engine="openpyxl")
        logger.info(f"Created new results file: {file_path}")

    except Exception as e:
        logger.exception(f"Error creating results file: {str(e)}")
        raise


def save_result_to_excel(
    file_path: str, resume_name: str, score: float, pros: str, cons: str
) -> None:
    """
    Save a resume evaluation result to the Excel file.

    Args:
        file_path: Path to the Excel file
        resume_name: Name of the resume file
        score: Average score (0-100)
        pros: Pros/strengths text
        cons: Cons/weaknesses text
    """
    try:
        # First check if file exists, if not initialize it
        if not os.path.exists(file_path):
            initialize_results_file(file_path)

        # Read existing data
        existing_df = pd.read_excel(file_path, engine="openpyxl")

        # Check if this resume is already in the file
        if resume_name in existing_df["File Name"].values:
            logger.info(f"Updating existing entry for {resume_name}")
            # Update the existing entry
            idx = existing_df[existing_df["File Name"] == resume_name].index[0]
            existing_df.loc[idx, "Average Score"] = score
            existing_df.loc[idx, "Pros"] = pros
            existing_df.loc[idx, "Cons"] = cons
        else:
            logger.info(f"Adding new entry for {resume_name}")
            # Create a new row
            new_row = pd.DataFrame(
                {
                    "File Name": [resume_name],
                    "Average Score": [score],
                    "Pros": [pros],
                    "Cons": [cons],
                }
            )
            # Append the new row
            existing_df = pd.concat([existing_df, new_row], ignore_index=True)

        # Sort by score in descending order
        existing_df = existing_df.sort_values("Average Score", ascending=False)

        # Save back to file
        existing_df.to_excel(file_path, index=False, engine="openpyxl")
        logger.info(f"Successfully saved results for {resume_name}")

    except Exception as e:
        logger.exception(f"Error saving results to Excel: {str(e)}")
        # Try to save just this resume in case the file is corrupted
        try:
            emergency_df = pd.DataFrame(
                {
                    "File Name": [resume_name],
                    "Average Score": [score],
                    "Pros": [pros],
                    "Cons": [cons],
                }
            )
            emergency_file = os.path.join(
                os.path.dirname(file_path), f"emergency_save_{resume_name}.xlsx"
            )
            emergency_df.to_excel(emergency_file, index=False, engine="openpyxl")
            logger.warning(f"Emergency save created at: {emergency_file}")
        except Exception as inner_e:
            logger.exception(f"Emergency save also failed: {str(inner_e)}")
            raise
