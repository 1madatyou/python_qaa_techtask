from typing import Optional

import requests
import pytest


@pytest.fixture
def state_url(base_url: str, server_state: Optional[bool]) -> str:
    return f"{base_url}/state"


def test_state(state_url: str):
    """
    Проверяет формат ответа с состоянием сервера.
    Ожидается код статуса 0 и состояние.
    """
    response = requests.get(state_url)
    assert response.status_code == 200
    assert response.json() == {'statusCode': 0, 'state': 'OК'}
