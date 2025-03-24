# Resume Screener

An automated tool for screening and evaluating resumes against job descriptions using AI.

## Overview

Resume Screener uses AI (Gemini 2.0 Flash and DeepSeek via OpenRouter) to evaluate candidate resumes against a job description. It extracts text from various document formats, generates a customizable scoring rubric, evaluates candidates, and saves results incrementally to an Excel file.

## Features

- **Multiple File Format Support**: Process .docx and .pdf resumes
- **Automated Rubric Generation**: AI-generated scoring rubric based on job description
- **Dual AI Evaluation**: Uses both Gemini 2.0 Flash and DeepSeek for balanced scoring
- **Pros & Cons Analysis**: Extracts strengths and areas for improvement
- **Incremental Result Saving**: Saves results immediately after each evaluation
- **Rate Limiting**: Respects API rate limits to prevent throttling
- **Robust Error Handling**: Continues processing despite individual file failures

## Prerequisites

- Python 3.8 or higher
- API Keys for:
  - Gemini API (for Gemini 2.0 Flash)
  - OpenRouter API (for DeepSeek access)

## Installation

1. Clone the repository or download the source code
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up API keys as environment variables:
   ```
   # On Windows
   set GEMINI_API_KEY=your_gemini_api_key
   set OPENROUTER_API_KEY=your_openrouter_api_key
   
   # On Linux/Mac
   export GEMINI_API_KEY=your_gemini_api_key
   export OPENROUTER_API_KEY=your_openrouter_api_key
   ```

## Usage

Run the main script:

```
python main.py
```

Follow the prompts to:
1. Enter the path to your job description file (.txt or .docx)
2. Enter the directory containing resumes (.docx and .pdf)
3. Review and optionally modify the generated scoring rubric
4. Wait for the processing to complete

Results will be saved to `resume_screening_results.xlsx` in the current directory.

## Output Format

The Excel output contains:
- Filename
- Average Score (0-100)
- Pros (bulleted list of strengths)
- Cons (bulleted list of areas for improvement)

Resumes are automatically sorted by score in descending order.

## API Information

### Gemini 2.0 Flash
This implementation uses Google's Gemini 2.0 Flash model which offers:
- 1M token context window for processing large documents
- Fast processing with high accuracy
- Used for generating rubrics and evaluating resumes

### DeepSeek (via OpenRouter)
The system accesses DeepSeek's models through OpenRouter:
- Uses the "deepseek/deepseek-chat:free" model
- Provides a complementary evaluation perspective
- Results are combined with Gemini's for a more balanced assessment

## Error Handling

- If a single resume fails to process, the application will continue with others
- Detailed logs are stored in the `logs` directory
- Emergency saves are created if the main Excel file becomes corrupted

## Rate Limiting

The application respects API rate limits:
- Maximum 10 requests per minute to each API
- Built-in pauses between resume processing to avoid throttling

## License

This project is open source and available under the MIT License.