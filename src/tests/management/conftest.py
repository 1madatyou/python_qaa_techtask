from typing import Tuple, Generator
import subprocess

import pytest

from tests.variables import (
    WEB_CALCULATOR_EXE,

    WEB_CALCULATOR_PORT,
    WEB_CALCULATOR_HOST,

    DEFAULT_HOST,
    DEFAULT_PORT
)

from .utils import run_command


@pytest.fixture(scope="module")
def start_app_custom() -> Generator[Tuple[str, str, str, str], None, None]:
    """Запускает приложение с указанными host и port"""
    host = WEB_CALCULATOR_HOST if WEB_CALCULATOR_HOST else "localhost"
    port = WEB_CALCULATOR_PORT if WEB_CALCULATOR_PORT else "5413"
    stdout, stderr = run_command("start", host, port)
    if "Сервер уже запущен" in stdout:
        pytest.skip("Сервер уже запущен")
    yield stdout, stderr, host, port
    subprocess.run([WEB_CALCULATOR_EXE, "stop"], check=True)


@pytest.fixture(scope="module")
def start_app_default() -> Generator[Tuple[str, str, str, str], None, None]:
    """Запускает приложение без указания host и port"""
    stdout, stderr = run_command("start")
    if "Сервер уже запущен" in stdout:
        pytest.skip("Сервер уже запущен")
    yield stdout, stderr, DEFAULT_HOST, DEFAULT_PORT
    subprocess.run([WEB_CALCULATOR_EXE, "stop"], check=True)


@pytest.fixture(scope="module", params=["default", "custom"])
def start_app(request) -> Generator[Tuple[str, str, str, str], None, None]:
    """Фикстура для запуска приложения в разных режимах"""
    fixture_func = request.getfixturevalue(f"start_app_{request.param}")

    yield fixture_func

    # Остановка приложения после завершения тестов
    subprocess.run([WEB_CALCULATOR_EXE, "stop"], check=True)
