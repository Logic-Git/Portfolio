import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path so tests can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock objects
@pytest.fixture
def mock_gemini_client():
    with patch('google.genai.Client') as mock_client:
        yield mock_client

@pytest.fixture
def mock_chroma_client():
    with patch('chromadb.Client') as mock_client:
        mock_collection = MagicMock()
        mock_client.return_value.get_collection.return_value = mock_collection
        mock_client.return_value.create_collection.return_value = mock_collection
        yield mock_client

@pytest.fixture
def mock_embedding_response():
    mock_response = MagicMock()
    mock_embedding = MagicMock()
    mock_embedding.values = [0.1, 0.2, 0.3]
    mock_response.embeddings = [mock_embedding]
    return mock_response