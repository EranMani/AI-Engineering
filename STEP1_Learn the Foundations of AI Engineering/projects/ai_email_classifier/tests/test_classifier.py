import pytest
from unittest.mock import Mock, patch
from src.classifier import classify_priority, classify_category, extract_email_info
from src.schemas import PriorityResult, CategoryResult, EmailInfoResult

@patch("src.classifier.client.responses.parse")
def test_classify_priority_success(mock_parse):
    fake_result = PriorityResult(priority="High", confidence=0.95)
    mock_response = Mock()
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response

    result = classify_priority("Urgent: Please review this ASAP!")

    assert result.priority == "High"
    assert result.confidence == 0.95
    mock_parse.assert_called_once()

@patch("src.classifier.client.responses.parse")
def test_classify_category_success(mock_parse):
    """Test successful category classification."""
    # Arrange
    fake_result = CategoryResult(category="Work", confidence=0.92)
    mock_response = Mock()
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response
    
    # Act
    result = classify_category("Meeting tomorrow at 2pm")
    
    # Assert
    assert result.category == "Work"
    assert result.confidence == 0.92
    mock_parse.assert_called_once()

@patch("src.classifier.client.responses.parse")
def test_extract_email_info_success(mock_parse):
    """Test successful email info extraction."""
    # Arrange
    fake_result = EmailInfoResult(
        sender_intent="Request for meeting",
        action_required=True,
        urgency_indicators=["ASAP", "urgent"],
        key_phrases=["meeting", "tomorrow"]
    )
    mock_response = Mock()
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response
    
    # Act
    result = extract_email_info("Can we meet tomorrow? It's urgent!")
    
    # Assert
    assert result.sender_intent == "Request for meeting"
    assert result.action_required is True
    assert len(result.urgency_indicators) == 2
    assert "ASAP" in result.urgency_indicators
    mock_parse.assert_called_once()

@patch("src.classifier.client.responses.parse")
def test_classify_priority_api_failure(mock_parse):
    """Test error handling when API fails."""
    # Arrange: Mock API failure
    mock_parse.side_effect = Exception("API Error")
    
    # Act & Assert: Should raise exception
    with pytest.raises(Exception, match="API Error"):
        classify_priority("Test email")