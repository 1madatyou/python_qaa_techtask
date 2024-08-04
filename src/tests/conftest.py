from typing import Optional, Generator, Tuple
import time
import subprocess

import pytest
import requests


WEB_CALCULATOR_EXE = "./../app/webcalculator.exe"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 17678


@pytest.fixture(scope="session")
def start_app() -> Generator[Tuple[str, str, str, str], None, None]:
    """Фикстура для запуска приложения"""
    result = subprocess.run(
        [WEB_CALCULATOR_EXE, "start"],
        check=True,
        capture_output=True,
        text=True
    )
    time.sleep(2)
    if "Сервер уже запущен" in result.stdout:
        pytest.skip("Сервер уже запущен.")

    yield result.stdout, result.stderr, DEFAULT_HOST, DEFAULT_PORT

    # Остановка приложения после завершения всех тестов
    subprocess.run([WEB_CALCULATOR_EXE, "stop"], check=True)


@pytest.fixture(scope="session")
def base_url(
    start_app: Generator[Tuple[str, str, str, str], None, None]
) -> str:
    """Фикстура базового url для запросов"""
    stdout, stderr, host, port = start_app
    return f"http://{host}:{port}/api"


@pytest.fixture(scope="session")
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
