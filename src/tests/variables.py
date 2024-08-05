import os

from dotenv import load_dotenv


# Определение текущей директории
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Путь к переменным окружения
dotenv_path = os.path.join(CURRENT_DIR, "../../.env")
# Загрузка переменных окружения
load_dotenv(dotenv_path)
# Путь к webcalculator.exe
WEB_CALCULATOR_EXE = os.path.join(CURRENT_DIR, "../app/webcalculator.exe")
# Параметры для host и port по умолчанию
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "17678"
# Параметры host и port из переменных окружения
WEB_CALCULATOR_HOST = os.getenv("WEB_CALCULATOR_HOST")
WEB_CALCULATOR_PORT = os.getenv("WEB_CALCULATOR_PORT")
