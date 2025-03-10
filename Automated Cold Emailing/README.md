# Automated Cold Emailing System

An AI-powered cold email automation system that researches target companies using Google's Gemini API and generates personalized cold emails based on templates.

## Features

- **Company Research:** Automatically researches target companies using Google's Gemini API with Google Search grounding
- **Email Generation:** Generates personalized initial and follow-up emails using AI
- **Email Management:** Handles the complete email workflow from generation to sending
- **Analytics:** Tracks email campaign performance
- **Robust Utilities:** CSV preprocessing, lead extraction, data cleaning, and more

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your API keys:
```
GOOGLE_API_KEY=your_google_api_key
```
4. Create an `Email-to-Credentials.xlsx` file mapping sender emails to Google API credential files

## File Structure

- `main.py`: Command-line interface for all functionality
- `research.py`: Functions for researching companies using Gemini API
- `email_generation.py`: Email content generation functionality
- `email_sending.py`: Email sending via Gmail API
- `utils.py`: Utility functions for data processing and management

## Usage

The system provides a command-line interface with various subcommands:

### Preprocess CSV Data

```bash
python main.py preprocess <csv_file> <columns...>
```

### Extract Lead Information

```bash
python main.py extract <csv_file> <excel_file> [--mapping MAPPING]
```

### Eliminate Incomplete Leads

```bash
python main.py eliminate <excel_file> <sheet_name> <columns...>
```

### Generate Emails

```bash
python main.py generate <excel_file> <template_file> --sender_name "Sender Name" [--row_start ROW] [--row_end ROW]
```

### Clean Email Content

```bash
python main.py clean <excel_file> <sheet_name> <columns...> --row_end ROW [--row_start ROW]
```

### Add Opt-out Messages

```bash
python main.py optout <excel_file> <sheet_name> <columns...> --row_end ROW [--row_start ROW]
```

### Verify Emails

```bash
python main.py verify <csv_file> <excel_file> [--output OUTPUT] [--excel_col COL] [--csv_col COL]
```

### Send Emails

```bash
python main.py send <excel_file> <sheet_name> <email_columns...> <sending_emails...> --sender_name "Sender Name" [--email_limit LIMIT] [--analytics_file FILE] [--analytics_sheet SHEET] [--analytics_cell CELL]
```

## Email Template Format

Email templates should be saved as text files with the initial email and follow-ups separated by `---`:

```
Initial email content here...
---
First follow-up email content here...
---
Second follow-up email content here...
```

## Configuration

### Gmail API Setup

1. Create a Google Cloud project
2. Enable the Gmail API
3. Create OAuth 2.0 credentials
4. Download the credentials JSON file
5. Add the mapping to your `Email-to-Credentials.xlsx` file

## Requirements

See `requirements.txt` for the complete list of dependencies.

## Privacy Note

The actual emails generated and sent using this system cannot be shared to preserve company privacy and comply with data protection regulations. This repository contains only the code used to build and run the email automation system.

## License

This project is licensed under the MIT License - see the LICENSE file for details.