from unittest.mock import MagicMock, patch
from service import analyze_text
from schemas import SentimentResult

def test_analyze_text_success():
    # 1. Create the fake data
    fake_data = SentimentResult(
        sentiment="Positive", 
        score=0.99, 
        key_points=["Works"]
    )
    
    # 2. Patch the exact method you are using
    with patch("service.client.responses.parse") as mock_parse:
        
        # 3. Setup Mock
        # Your code calls: response.output_text
        mock_response = MagicMock()
        mock_response.output_text = fake_data
        mock_parse.return_value = mock_response

        # 4. Run Logic
        result = analyze_text("Test")

        # 5. Verify
        assert result.sentiment == "Positive"
        mock_parse.assert_called_once()