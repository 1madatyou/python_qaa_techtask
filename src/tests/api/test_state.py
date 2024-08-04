import requests
import pytest


@pytest.fixture
def state_url(base_url, server_state):
    return f"{base_url}/state"


def test_state(state_url):
    """
    Проверяет формат ответа с состоянием сервера.
    Ожидается код статуса 0 и состояние.
    """
    response = requests.get(state_url)
    assert response.status_code == 200
    assert response.json() == {'statusCode': 0, 'state': 'OК'}
