# app/tests/test_redis_utils.py
from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from app.utils.redis_utils import (add_to_redis, delete_from_redis,
                                   is_key_in_redis)


@pytest.fixture
def mock_redis_client(mocker):
    mock_client = MagicMock()
    mocker.patch("app.utils.redis_utils.redis_client", mock_client)
    return mock_client


def test_add_and_check_redis(mock_redis_client):
    mock_redis_client.exists.return_value = True

    add_to_redis("test_key", "test_value", timedelta(minutes=5))

    mock_redis_client.set.assert_called_once_with("test_key", "test_value", ex=300)
    assert is_key_in_redis("test_key") is True


def test_delete_from_redis(mock_redis_client):
    # Configura el mock para devolver False después del borrado
    def exists_side_effect(key):
        if mock_redis_client.delete.call_count == 0:
            return 1  # Existe antes de borrar
        return 0  # No existe después de borrar

    mock_redis_client.exists.side_effect = exists_side_effect

    delete_from_redis("test_key")
    mock_redis_client.delete.assert_called_once_with("test_key")
    assert is_key_in_redis("test_key") is False
