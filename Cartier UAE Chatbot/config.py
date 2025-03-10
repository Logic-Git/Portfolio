import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
KNOWLEDGE_BASE_DIR = os.getenv("KNOWLEDGE_BASE_DIR", "./data")

# Parameters for document splitting
CHUNK_SIZE = 300
CHUNK_OVERLAP = 100

# ChromaDB collection name
COLLECTION_NAME = "customer_support_docs"

# Query parameters
MAX_RESULTS = 20  # Maximum number of results to return from knowledge base queries

# Conversation parameters
CONVERSATION_HISTORY_LENGTH = (
    3  # Number of previous conversations to maintain for context
)
