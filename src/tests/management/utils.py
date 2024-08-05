from typing import Tuple
import subprocess
import time

from tests.variables import WEB_CALCULATOR_EXE


def run_command(command: str, *args: str) -> Tuple[str, str]:
    """Запускает команду с задержкой и возвращает выводы stdout stderr"""
    result = subprocess.run(
        [WEB_CALCULATOR_EXE, command] + list(args),
        capture_output=True,
        text=True
    )
    time.sleep(2)
    return result.stdout, result.stderr
