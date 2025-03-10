import pytest
from unittest.mock import patch, MagicMock
from embeddings import get_embedding


@patch("embeddings.gemini_client")
def test_get_embedding_success(mock_client):
    """Test that get_embedding returns the expected embedding when API call succeeds"""
    # Create a mock response with the expected structure
    mock_response = MagicMock()
    mock_embedding = MagicMock()
    mock_embedding.values = [0.1, 0.2, 0.3]
    mock_response.embeddings = [mock_embedding]

    # Configure the mock to return our prepared response
    mock_client.models.embed_content.return_value = mock_response

    # Call the function
    result = get_embedding("test text")

    # Assert that the function was called correctly
    mock_client.models.embed_content.assert_called_once_with(
        model="text-embedding-004", contents=["test text"]
    )

    # Assert that the correct embedding was returned
    assert result == [0.1, 0.2, 0.3]


@patch("embeddings.gemini_client")
def test_get_embedding_exception(mock_client):
    """Test that get_embedding handles exceptions properly"""
    # Configure the mock to raise an exception
    mock_client.models.embed_content.side_effect = Exception("API error")

    # Call the function and check that it handles the exception
    result = get_embedding("test text")

    # Function should return an empty list on error
    assert result == []
