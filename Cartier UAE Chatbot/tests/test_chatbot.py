import pytest
from unittest.mock import patch, MagicMock
from chatbot import Chatbot
from config import CONVERSATION_HISTORY_LENGTH, MAX_RESULTS


@pytest.fixture
def chatbot():
    return Chatbot()


@pytest.fixture
def chatbot_with_history():
    bot = Chatbot()
    bot.history = [
        {"user": "Hello", "agent": "Hi there!"},
        {"user": "How are you?", "agent": "I'm doing well, how can I help you?"},
        {
            "user": "Tell me about Cartier",
            "agent": "Cartier is a luxury jewelry brand.",
        },
    ]
    return bot


def test_get_recent_history(chatbot_with_history):
    """Test that get_recent_history returns correct formatted history using config value"""
    result = (
        chatbot_with_history.get_recent_history()
    )  # Using default CONVERSATION_HISTORY_LENGTH
    expected = "User: Hello\nAgent: Hi there!\nUser: How are you?\nAgent: I'm doing well, how can I help you?\nUser: Tell me about Cartier\nAgent: Cartier is a luxury jewelry brand.\n"
    assert result == expected


def test_get_recent_history_with_empty_history(chatbot):
    """Test that get_recent_history handles empty history gracefully"""
    result = chatbot.get_recent_history()
    assert result == ""


@patch("chatbot.gemini_client")
def test_enhance_query(mock_gemini_client, chatbot):
    """Test the enhance_query method"""
    # Setup mock
    mock_response = MagicMock()
    mock_response.text = "Enhanced query text"
    mock_gemini_client.models.generate_content.return_value = mock_response

    # Test with no history
    result = chatbot.enhance_query("test query")
    mock_gemini_client.models.generate_content.assert_called_once()
    assert result == "Enhanced query text"

    # Test with history
    mock_gemini_client.models.generate_content.reset_mock()
    result = chatbot.enhance_query("test query", history="Previous conversation")
    mock_gemini_client.models.generate_content.assert_called_once()
    assert result == "Enhanced query text"


@patch("chatbot.gemini_client")
def test_enhance_query_exception(mock_gemini_client, chatbot):
    """Test enhance_query exception handling"""
    mock_gemini_client.models.generate_content.side_effect = Exception("API error")

    # Should return original query on error
    result = chatbot.enhance_query("test query", history="Previous conversation")
    assert result == "test query"


@patch("chatbot.gemini_client")
def test_summarize_context(mock_gemini_client, chatbot):
    """Test the summarize_context method"""
    # Setup mock
    mock_response = MagicMock()
    mock_response.text = "Summarized context"
    mock_gemini_client.models.generate_content.return_value = mock_response

    result = chatbot.summarize_context("history", "query")

    # Verify that Gemini client was called correctly
    mock_gemini_client.models.generate_content.assert_called_once()
    assert result == "Summarized context"


@patch("chatbot.gemini_client")
def test_summarize_context_exception(mock_gemini_client, chatbot):
    """Test summarize_context exception handling"""
    mock_gemini_client.models.generate_content.side_effect = Exception("API error")

    result = chatbot.summarize_context("history", "query")

    # Should return original history on error
    assert result == "history"


@patch("chatbot.query_knowledge")
@patch("chatbot.gemini_client")
def test_generate_answer(mock_gemini_client, mock_query_knowledge, chatbot):
    """Test the generate_answer method"""
    # Setup mocks for all Gemini responses
    mock_enhance_response = MagicMock()
    mock_enhance_response.text = "Enhanced query text"

    mock_summary_response = MagicMock()
    mock_summary_response.text = "Summarized context"

    mock_final_response = MagicMock()
    mock_final_response.text = "Generated answer"

    # Setup the response sequence for generate_content
    mock_gemini_client.models.generate_content.side_effect = [
        mock_enhance_response,  # For enhance_query
        mock_summary_response,  # For summarize_context
        mock_final_response,  # For final answer
    ]

    # Setup query_knowledge mock
    mock_query_knowledge.return_value = ["Document 1", "Document 2"]

    # Call the method
    result = chatbot.generate_answer("test question")

    # Verify enhance_query was called first and its result was used for query_knowledge
    mock_query_knowledge.assert_called_once_with(
        "Enhanced query text", n_results=MAX_RESULTS
    )

    # Verify the final response was used
    assert result == "Generated answer"

    # Verify history was updated correctly
    assert len(chatbot.history) == 1
    assert chatbot.history[0]["user"] == "test question"
    assert chatbot.history[0]["agent"] == "Generated answer"
