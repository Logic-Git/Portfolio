import pytest
from unittest.mock import patch, mock_open, MagicMock, call
import os
from ingest_database import load_documents, chunk_text, index_documents


def test_chunk_text():
    """Test that the chunk_text function correctly chunks a text"""
    text = "This is a test document that needs to be chunked for processing."
    chunk_size = 10
    chunk_overlap = 3

    result = chunk_text(text, chunk_size, chunk_overlap)

    # Expected chunks based on character-based chunking with size 10 and overlap 3
    expected = [
        "This is a ",
        " a test do",
        " document ",
        "nt that ne",
        " needs to ",
        "to be chun",
        "hunked for",
        "for proces",
        "cessing.",
        ".",
    ]

    assert result == expected


@patch("glob.glob")
@patch("builtins.open", new_callable=mock_open, read_data="Document content")
def test_load_documents(mock_file, mock_glob):
    """Test that load_documents correctly loads files from directory"""
    mock_glob.return_value = ["/path/to/file1.txt", "/path/to/file2.txt"]

    result = load_documents("/path/to/docs")

    mock_glob.assert_called_once_with(os.path.join("/path/to/docs", "*.txt"))
    assert mock_file.call_count == 2

    expected = [
        {"content": "Document content", "source": "/path/to/file1.txt"},
        {"content": "Document content", "source": "/path/to/file2.txt"},
    ]
    assert result == expected


@patch("ingest_database.load_documents")
@patch("ingest_database.get_embedding")
@patch("ingest_database.chromadb.PersistentClient")
@patch("uuid.uuid4")
def test_index_documents(
    mock_uuid4, mock_chroma_client, mock_get_embedding, mock_load_documents
):
    """Test that index_documents correctly processes and indexes documents"""
    # Setup mocks
    mock_load_documents.return_value = [
        {"content": "This is document 1", "source": "file1.txt"},
        {"content": "This is document 2", "source": "file2.txt"},
    ]

    # Create a mock 768-dimensional embedding
    mock_embedding = [0.1] * 768
    mock_get_embedding.return_value = mock_embedding
    mock_uuid4.side_effect = ["id1", "id2", "id3", "id4"]

    # Setup the mock ChromaDB client
    mock_collection = MagicMock()
    mock_chroma_client.return_value.get_collection.return_value = mock_collection
    mock_chroma_client.return_value.create_collection.return_value = mock_collection

    # Call the function
    index_documents()

    # Check that documents were loaded
    mock_load_documents.assert_called_once()

    # Verify that embeddings were generated (one for each chunk from the documents)
    assert mock_get_embedding.call_count >= 2

    # Verify that documents were added to the collection
    mock_collection.add.assert_called_once()

    # Check that the arguments passed to add include documents, embeddings, metadatas, and ids
    call_args = mock_collection.add.call_args[1]
    assert "documents" in call_args
    assert "embeddings" in call_args
    assert "metadatas" in call_args
    assert "ids" in call_args
