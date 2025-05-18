import pytest
from fastapi import Request
from app.auth import verify_token
import asyncio

def test_verify_token_valid(mocker):
    mock_request = mocker.Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer valid_token"}
    
    mock_verify = mocker.patch("app.auth.auth.verify_id_token")
    mock_verify.return_value = {"uid": "user123"}
    
    user_data = asyncio.run(verify_token(mock_request))
    assert user_data["uid"] == "user123"

def test_verify_token_invalid(mocker):
    mock_request = mocker.Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer invalid_token"}
    
    mocker.patch("app.auth.auth.verify_id_token", side_effect=Exception("Invalid token"))
    
    with pytest.raises(Exception):
        asyncio.run(verify_token(mock_request))
