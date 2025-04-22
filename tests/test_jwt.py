from app.core.security import decode_token
from app.utils.jwt import create_access_token


def test_create_and_decode_token():
    data = {"sub": "test@yopmail.com"}
    token = create_access_token(data)
    payload = decode_token(token)
    assert payload["sub"] == data["sub"]
