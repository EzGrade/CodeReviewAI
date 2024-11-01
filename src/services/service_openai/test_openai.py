import pytest
from openai import AuthenticationError
from services.service_openai.service import OpenAi
import config


def test_get_openai_client():
    openai_instance = OpenAi([], api_key=config.OPENAI_API_KEY)
    client = openai_instance.get_openai_client()

    assert client is not None

    model = "gpt-3.5-turbo-0125"
    response = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': 'Hello!'}]
    )
    assert response is not None


def test_invalid_api_key():
    invalid_api_key = "invalid_api_key"
    openai_instance = OpenAi([], api_key=invalid_api_key)
    client = openai_instance.get_openai_client()

    with pytest.raises(AuthenticationError):
        client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{'role': 'user', 'content': 'Hello!'}]
        )
