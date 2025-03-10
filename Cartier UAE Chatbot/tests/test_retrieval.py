import pytest
from unittest.mock import patch, MagicMock
from retrieval import query_knowledge
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE


@pytest.fixture
def mock_query_result():
    return {
        "documents": [["doc1", "doc2", "doc3"]],
        "metadatas": [
            [{"source": "file1.txt"}, {"source": "file2.txt"}, {"source": "file3.txt"}]
        ],
        "distances": [[0.1, 0.2, 0.3]],
        "ids": [["id1", "id2", "id3"]],
    }


@patch("retrieval.get_embedding")
@patch("retrieval.chromadb.PersistentClient")
def test_query_knowledge(mock_persistent_client, mock_get_embedding, mock_query_result):
    """Test that query_knowledge returns the expected documents"""
    # Configure mocks
    mock_embedding = [0.1] * 768  # Create a 768-dimensional embedding
    mock_get_embedding.return_value = mock_embedding
    mock_collection = MagicMock()
    mock_collection.query.return_value = mock_query_result
    mock_persistent_client.return_value.get_collection.return_value = mock_collection

    # Call function
    result = query_knowledge("test query", n_results=3)

    # Verify function calls
    mock_get_embedding.assert_called_once_with("test query")

    # Verify PersistentClient was initialized correctly
    mock_persistent_client.assert_called_once()
    mock_persistent_client.return_value.get_collection.assert_called_once_with(
        name="customer_support_docs"
    )

    # Verify query was called with correct parameters
    mock_collection.query.assert_called_once_with(
        query_embeddings=[mock_embedding],
        n_results=3,
        include=["documents", "metadatas"],
    )

    # Verify return value
    assert result == ["doc1", "doc2", "doc3"]
