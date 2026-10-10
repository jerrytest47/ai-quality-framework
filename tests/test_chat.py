
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)



def test_chat_returns_200():
    mock_response = MagicMock()
    mock_response.output_text = (
        "Returns are accepted within 30 days."
    )

    # Provide a fake API key for the test
    with patch.dict(
        "os.environ",
        {"OPENAI_API_KEY": "fake-test-key"}
    ):
        # Mock the OpenAI client
        with patch("app.main.OpenAI") as mock_openai:
            mock_openai.return_value.responses.create.return_value = (
                mock_response
            )

            response = client.post(
                "/chat",
                json={
                    "message": "What is your return policy?"
                }
            )

    assert response.status_code == 200
    assert response.json()["answer"] == (
        "Returns are accepted within 30 days."
    )



def test_chat_requires_message():
    response = client.post(
        "/chat",
        
        json={}
    )

    assert response.status_code == 422
