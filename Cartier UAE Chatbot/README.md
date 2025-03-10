# Cartier UAE Customer Support Chatbot

A specialized customer support chatbot designed exclusively for Cartier UAE operations. The chatbot provides detailed information about Cartier's product catalog in the UAE, including fragrances, watches, and jewelry, as well as UAE-specific policies like shipping, returns, and warranty services.

## Technical Overview

This chatbot implements a Retrieval Augmented Generation (RAG) approach using the following components:

1. **Knowledge Base**: The system uses a collection of text files in the `data/` directory containing information about Cartier UAE's products and policies.

2. **Vector Database**: ChromaDB is used to store and retrieve vectorized chunks of the knowledge base. The texts are split into manageable chunks and embedded using Google's Gemini text-embedding-004 model.

3. **Query Processing Pipeline**:
   - **Query Enhancement**: 
     - Improves query quality through spelling correction and grammar fixes
     - Completes incomplete sentences based on context
     - Incorporates relevant keywords from conversation history
     - Preserves original intent while optimizing for vector search
     - Uses Gemini's language understanding to maintain semantic accuracy

   - **Vector Search**:
     - Converts enhanced queries into embeddings using Gemini's text-embedding-004 model
     - Performs similarity search in ChromaDB to find relevant knowledge chunks
     - Returns top 20 most relevant context pieces (configurable via MAX_RESULTS)

   - **Context Summarization**:
     - Combines retrieved knowledge chunks with conversation history
     - Uses Gemini to create a concise summary that maintains key information
     - Ensures the summary captures both historical context and current query relevance

   - **Response Generation**:
     - Constructs a detailed prompt combining summarized context and user query
     - Uses Gemini to generate responses strictly based on provided knowledge
     - Implements guardrails to:
       - Reject queries unrelated to Cartier UAE
       - Acknowledge when information is not available in the knowledge base
       - Handle common conversational elements (greetings, farewells)

4. **Conversation Management**:
   - Maintains a history of the last 3 conversation turns (configurable)
   - Each turn includes both user input and agent response
   - History is used to:
     - Provide context for query enhancement
     - Resolve ambiguous references in follow-up questions
     - Maintain conversation coherence
     - Track conversation state for contextual responses

## Prerequisites

- Python 3.9 or higher
- Google Cloud Project with Gemini API access
- Git

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AStudio-Chatbot
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following content:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   CHROMA_PERSIST_DIR=./chroma_db
   KNOWLEDGE_BASE_DIR=./data
   ```

4. Initialize the knowledge base by running:
   ```bash
   python ingest_database.py
   ```
   Make sure that your directory given by the path assigned to CHROMA_PERSIST_DIR exists in your repository. In the default case, this means make sure that the chroma_db directory is in the repository.
   This will process the documents in the `data/` directory and create the vector database. Note that running this script will add to the existing ChromaDB collection if one exists. For a fresh start, you may want to delete the `chroma_db` directory before running this script.

5. Start the chatbot:
   ```bash
   python chatbot.py
   ```

## Running Tests

The project includes a comprehensive test suite. To run the tests:

```bash
pytest tests/
```

## Project Structure

- `chatbot.py`: Main chatbot implementation with conversation handling
- `config.py`: Configuration settings and environment variables
- `embeddings.py`: Text embedding generation using Gemini
- `ingest_database.py`: Knowledge base ingestion and vector database creation
- `retrieval.py`: Vector similarity search and context retrieval
- `data/`: Contains the knowledge base text files
  - `policies.txt`: Cartier UAE policies and procedures
  - `products.txt`: Product catalog and pricing information
- `tests/`: Unit tests for all components

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `CHROMA_PERSIST_DIR`: Directory for ChromaDB persistence (default: ./chroma_db)
- `KNOWLEDGE_BASE_DIR`: Directory containing knowledge base documents (default: ./data)

## Use Cases

This chatbot is specifically designed to handle queries about:
- Cartier UAE's product catalog and pricing
- UAE-specific shipping and delivery policies
- Return and exchange procedures in the UAE
- UAE warranty and product authenticity verification
- Customer service contact information for UAE operations
- Local payment methods and security measures

## Note

Make sure to obtain a Gemini API key from Google Cloud Console and add it to your `.env` file before running the chatbot. The `.env` file is included in `.gitignore` for security.