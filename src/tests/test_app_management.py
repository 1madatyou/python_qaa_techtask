from typing import Tuple, Generator
import subprocess
import time

import pytest
import requests


WEB_CALCULATOR_EXE = "./../app/webcalculator.exe"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 17678


def run_command(command: str, *args: str) -> Tuple[str, str]:
    """Запускает команду с задержкой и возвращает выводы stdout stderr"""
    result = subprocess.run(
        [WEB_CALCULATOR_EXE, command] + list(args),
        check=True,
        capture_output=True,
        text=True
    )
    time.sleep(2)
    return result.stdout, result.stderr


@pytest.fixture(scope="module")
def start_app_custom() -> Generator[Tuple[str, str, str, str], None, None]:
    """Запускает приложение с указанными host и port"""
    host = "localhost"
    port = "5413"
    stdout, stderr = run_command("start", host, port)
    if "Сервер уже запущен" in stdout:
        pytest.skip("Сервер уже запущен")
    yield stdout, stderr, host, port
    subprocess.run([WEB_CALCULATOR_EXE, "stop"], check=True)


@pytest.mark.parametrize("help_arg", ["-h", "--help"])
def test_help(help_arg: str):
    """Тест команды help"""
    stdout, stderr = run_command(help_arg)
    expected_lines = [
        "usage",
        "positional arguments",
        "start",
        "stop",
        "restart",
        "show_log",
        "optional arguments",
        "-h, --help"
    ]
    for line in expected_lines:
        assert line in stdout, f"Отсутствует ожидаемая строка: {line}"


@pytest.mark.parametrize(
    "command, help_arg",
    [("start", "-h"), ("start", "--help")]
)
def test_detailed_help(command: str, help_arg: str):
    """Тест детализированного вывода команды help для конкретных команд."""
    stdout, stderr = run_command(command, help_arg)
    if command == "start":
        expected_detailed_lines = [
            "usage: webcalculator.exe start [-h] [host] [port]",
            "positional arguments:",
            "host",
            "port",
            "optional arguments",
            "-h, --help",
        ]
        for line in expected_detailed_lines:
            assert line in stdout, f"Отсутствует ожидаемая строка: {line}"


def test_default_start(
    start_app: Generator[Tuple[str, str, str, str], None, None]
):
    """Тест запуска приложения без аргументов"""
    stdout, stderr, host, port = start_app
    response = requests.get(f"http://{host}:{port}/api/state")
    assert response.status_code == 200
    assert "Запуск Веб-калькулятора на 127.0.0.1:17678" in stdout
    assert "Веб-калькулятор запущен на 127.0.0.1:17678" in stdout


def test_start_already_running(
        start_app: Generator[Tuple[str, str, str, str], None, None]
):
    """Тест запуска приложения в ситуации, когда оно уже запущено"""
    stdout, stderr = run_command("start")
    assert "Сервер уже запущен" in stdout


def test_show_log(
    start_app: Generator[Tuple[str, str, str, str], None, None]
):
    """Тест команды show_log"""
    stdout, stderr, host, port = start_app
    show_log_stdout, show_log_stderr = run_command("show_log")
    assert show_log_stdout, "Лог файл пустой"
    expected_lines = [
        f"Веб-калькулятор запущен на {host}:{port}",
    ]
    for line in expected_lines:
        assert line in show_log_stdout, f"Ожидаемая строка отсутствует:{line}"


def test_restart(start_app: Generator[Tuple[str, str, str, str], None, None]):
    """Тест команды restart"""
    stdout, stderr, host, port = start_app
    restart_stdout, restart_stderr = run_command("restart")
    print(stdout)
    assert "Веб-калькулятор остановлен" in restart_stdout
    assert f"Запуск Веб-калькулятора на {host}:{port}" in restart_stdout
    assert f"Веб-калькулятор запущен на {host}:{port}" in restart_stdout


def test_stop(start_app: Generator[Tuple[str, str, str, str], None, None]):
    """Тест команды stop"""
    stdout, stderr = run_command("stop")
    assert "Пытаемся остановить Веб-калькулятор" in stdout
    assert "Веб-калькулятор остановлен" in stdout


def test_custom_start(
    start_app_custom: Generator[Tuple[str, str, str, str], None, None]
):
    """Тест запуска приложения с аргументами (host, port)"""
    stdout, stderr, host, port = start_app_custom
    response = requests.get(f"http://{host}:{port}/api/state")
    assert f"Запуск Веб-калькулятора на {host}:{port}" in stdout
    assert f"Веб-калькулятор запущен на {host}:{port}" in stdout
    assert response.status_code == 200
