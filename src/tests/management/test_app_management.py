from typing import Tuple, Generator
import os

import pytest
import requests

from .utils import run_command


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
    [("start", "-h"),
     ("start", "--help")]
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


def test_show_log():
    """Тест команды show_log"""
    log_path = os.path.join(
        os.getenv("LOCALAPPDATA"), "webcalculator", "webcalculator.log"
    )
    show_log_stdout, show_log_stderr = run_command("show_log")
    with open(log_path, 'r') as log_file:
        logs = log_file.read()
    # Сравниваем вывод команды и текст лог-файла без пробельных символов
    # в конце и начале строк
    assert show_log_stdout.strip() == logs.strip()


def test_start(
    start_app: Generator[Tuple[str, str, str, str], None, None]
):
    """Тест запуска приложения без аргументов"""
    stdout, stderr, host, port = start_app
    response = requests.get(f"http://{host}:{port}/api/state")
    assert response.status_code == 200
    assert f"Запуск Веб-калькулятора на {host}:{port}" in stdout
    assert f"Веб-калькулятор запущен на {host}:{port}" in stdout


def test_start_already_running(
    start_app: Generator[Tuple[str, str, str, str], None, None]
):
    """Тест запуска приложения в ситуации, когда оно уже запущено"""
    stdout, stderr = run_command("start")
    assert "Сервер уже запущен" in stdout


def test_restart(start_app: Generator[Tuple[str, str, str, str], None, None]):
    """Тест команды restart"""
    stdout, stderr, host, port = start_app
    restart_stdout, restart_stderr = run_command("restart")
    assert "Веб-калькулятор остановлен" in restart_stdout
    assert f"Запуск Веб-калькулятора на {host}:{port}" in restart_stdout
    assert f"Веб-калькулятор запущен на {host}:{port}" in restart_stdout


def test_stop(start_app: Generator[Tuple[str, str, str, str], None, None]):
    """Тест команды stop"""
    stdout, stderr = run_command("stop")
    assert "Пытаемся остановить Веб-калькулятор" in stdout
    assert "Веб-калькулятор остановлен" in stdout


def test_restart_when_already_stopped():
    """Тест команды restart, когда сервер уже остановлен или не запущен"""
    stdout, stderr = run_command("restart")
    print(stderr, stdout)
    assert 'Веб-калькулятор не запущен. Используйте команду "start"' in stdout
