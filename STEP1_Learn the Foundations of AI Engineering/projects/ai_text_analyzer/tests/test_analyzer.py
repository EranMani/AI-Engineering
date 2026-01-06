import pytest
from unittest.mock import Mock, patch
from src.analyzer import analyze_sentiment, analyze_summary, analyze_topics
from src.schemas import SentimentResult, SummaryResult, TopicResult

@patch("src.analyzer.client.responses.parse")
def test_analyze_sentiment_success(mock_parse):
    # Arrange: Create fake response
    fake_result = SentimentResult(sentiment="positive", score=0.95)
    mock_response = Mock()

    # output_text should return a json string (what the real api returns)
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response

    # Act: call function
    result = analyze_sentiment("I love this!")

    # Assert
    assert result.sentiment == "positive"
    assert result.score == 0.95
    mock_parse.assert_called_once()

@patch("src.analyzer.client.responses.parse")
def test_analyze_summary_success(mock_parse):
    fake_result = SummaryResult(
        summary="This is a test summary",
        key_points=["Point 1", "Point 2"]
    )

    mock_response = Mock()
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response

    result = analyze_summary("Test text for summary")

    assert result.summary == "This is a test summary"
    assert len(result.key_points) == 2
    mock_parse.assert_called_once()

@patch("src.analyzer.client.responses.parse")
def test_analyze_topics_success(mock_parse):
    fake_result = TopicResult(
        topics=["AI", "Python", "Testing"],
        primary_topic="AI"
    )

    mock_response = Mock()
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response

    result = analyze_topics("Test text about AI and Python")

    assert "AI" in result.topics
    assert result.primary_topic == "AI"
    mock_parse.assert_called_once()
