from typing import Optional

import pytest
import requests


# Фикстура базового url в рамках сессии тестирования
@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://localhost:5413/api"


# Фикстура проверки состояния сервера
@pytest.fixture(scope="session")
def server_state(base_url: str) -> Optional[bool]:
    """
    Проверяет состояние сервера перед выполнением тестов.
    Если состояние сервера некорректное, пропускает все тесты, зависящие от этой фикстуры.
    Возвращает True, если сервер в корректном состоянии, иначе False.
    """
    try:
        response = requests.get(f"{base_url}/state")
        if (response.status_code == 200 and 
            response.json() == {'statusCode': 0, 'state': 'OК'}):
            return True
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения с сервером.")
    pytest.skip("Ошибка состояния сервера. Пропускаем тесты.")
        