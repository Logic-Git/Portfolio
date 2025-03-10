"""
Research module for the automated cold emailing system.
Provides functions for researching companies using Google's Gemini API.
"""

import os
import logging
from utils import rate_limit
import google.generativeai as genai
from google import genai as genai_full
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Configure Google API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


@rate_limit(calls_per_minute=10)
def extract_company_info_for_campaign(template_email, template_email_sequence):
    """
    Extracts information about your company and its offerings from the
    email templates using the Gemini 1.0 Pro API.

    Args:
        template_email: The initial email template (string).
        template_email_sequence: A list of follow-up email templates (strings).

    Returns:
        A string containing the extracted information about your company,
        or None if an error occurred.
    """
    model = genai.GenerativeModel("gemini-1.0-pro")
    email_chain = f"Initial Email:\n{template_email}\n\n"
    for i, email in enumerate(template_email_sequence):
        email_chain += f"Follow-up Email {i + 1}:\n{email}\n\n"

    prompt = f"""
    You are a market research assistant. I will provide you with email
    templates (initial email and follow-ups) that my company uses for
    marketing campaigns.

    Please analyze the email templates and extract all information related
    to my company, including:

    - The name of my company.
    - The products or services we are offering/selling in this specific
      campaign.
    - The key features, advantages, and benefits of our offerings as
      described in the emails.
    - Any value propositions or claims made about our company or offerings.
    - Any other relevant details about my company that are mentioned in
      the emails.

    Here are the email templates:

    ```
    {email_chain}
    ```

    Please provide a concise summary of the extracted information about 
    my company, focusing on details that would be relevant for further 
    marketing and outreach efforts.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error during Gemini API request: {e}")
        return None


@rate_limit(calls_per_minute=10)
def research_company_with_gemini(company_name, your_company_info):
    """
    Researches a company using the Gemini API with Google Search grounding.

    Args:
        company_name: The name of the company to research.
        your_company_info: Information about your company and the services you offer.

    Returns:
        A string containing the company research information, or None if an error occurred.
    """
    client = genai_full.Client(api_key=GOOGLE_API_KEY)
    model_id = "gemini-2.0-flash-exp"

    google_search_tool = Tool(google_search=GoogleSearch())

    prompt = f"""
    You are a market research assistant.
    I need you to find information about the company "{company_name}".

    I will be using this information for marketing purposes, specifically to tailor
    email outreach for my company.

    Here's a bit about what my company does:
    ```
    {your_company_info}
    ```

    Please provide me with relevant information about "{company_name}",
    keeping in mind what we offer. Focus on details that might be useful for
    crafting a personalized email, such as:

    - The company's industry and what they do.
    - Any recent news or announcements about the company.
    - Information about their potential needs or challenges that our services
      could address.
    - Any other relevant details that might be helpful for marketing purposes.

    Please use your ability to access and process web information to gather
    the most up-to-date and relevant details about {company_name}.
    """
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=GenerateContentConfig(
                tools=[google_search_tool], response_modalities=["TEXT"]
            ),
        )

        # Assuming you want the full text from all parts
        full_text = "".join(
            [part.text for part in response.candidates[0].content.parts]
        )
        return full_text

    except Exception as e:
        logging.error(f"Error during Gemini API request: {e}")
        return None
