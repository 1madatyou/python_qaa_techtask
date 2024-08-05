from typing import Optional, Generator, Tuple
import time
import subprocess

import pytest
import requests

from tests.variables import (
    WEB_CALCULATOR_EXE,

    WEB_CALCULATOR_PORT,
    WEB_CALCULATOR_HOST,

    DEFAULT_HOST,
    DEFAULT_PORT
)


@pytest.fixture(scope="module")
def start_app() -> Generator[Tuple[str, str, str, str], None, None]:
    """Фикстура для запуска приложения и тестирования API"""
    command = [WEB_CALCULATOR_EXE, "start"]
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    if WEB_CALCULATOR_HOST and WEB_CALCULATOR_PORT:
        # Если в переменных окружения размещены хост и порт, то
        # запускаем с их указанием
        host = WEB_CALCULATOR_HOST
        port = WEB_CALCULATOR_PORT
        command.extend([WEB_CALCULATOR_HOST, WEB_CALCULATOR_PORT])
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )
    time.sleep(2)

    if "Сервер уже запущен" in result.stdout:
        pytest.skip("Сервер уже запущен.")

    yield result.stdout, result.stderr, host, port

    # Остановка приложения после завершения всех тестов
    subprocess.run([WEB_CALCULATOR_EXE, "stop"], check=True)


@pytest.fixture(scope="module")
def base_url(
    start_app: Generator[Tuple[str, str, str, str], None, None]
) -> str:
    """Фикстура базового url для запросов"""
    stdout, stderr, host, port = start_app
    return f"http://{host}:{port}/api"


@pytest.fixture(scope="module")
def server_state(base_url: str) -> Optional[bool]:
    """
    Проверяет состояние сервера перед выполнением тестов.
    Если состояние сервера некорректное, пропускает все тесты,
    зависящие от этой фикстуры.
    Возвращает True, если сервер в корректном состоянии.
    """
    try:
        response = requests.get(f"{base_url}/state")
        if (response.status_code == 200 and
                response.json() == {'statusCode': 0, 'state': 'OК'}):
            return True
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения с сервером.")
    pytest.skip("Ошибка состояния сервера. Пропускаем тесты.")
