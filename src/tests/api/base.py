from abc import ABC
from typing import Dict, Optional, Any, Union
import json

import pytest
import requests

from .constants import INT32_MAX, INT32_MIN


class BaseOperationTest(ABC):
    """Базовый класс для тестирования эндпоинтов с вычислениями"""

    operation = None

    def make_request(
        self, operation_url: str, data: Dict[str, Any]
    ) -> requests.Response:
        data_as_json = json.dumps(data)
        response = requests.post(operation_url, data=data_as_json)
        return response

    @pytest.fixture(scope="class")
    def operation_url(
        self, base_url: str, server_state: Optional[bool]
    ) -> str:
        """Формирует url запроса"""
        return f"{base_url}/{self.operation}"

    @pytest.mark.skip(reason="Должен быть переопределен в дочернем классе")
    @pytest.mark.parametrize(
        "data, expected_result",
        []
    )
    def test_operation_success(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, int],
        operation_url: str
    ):
        """
        Проверяет обработку успешных случаев.
        Ожидается возвращение кода статуса 0 с результатом.

        Должен быть переопределен в дочернем классе, т.к. должен реализовать
        свои собственные варианты входных данных чтобы протестировать
        конкретную логику, связанную с его функциональностью.
        """
        response = self.make_request(operation_url, data)
        assert response.status_code == 200
        assert response.json() == expected_result, (
            f"Ожидалось: {expected_result},\n"
            f"получено: {response.json()}"
        )

    @pytest.mark.skip(reason="Должен быть переопределен в дочернем классе")
    @pytest.mark.parametrize(
        "data, expected_result",
        []
    )
    def test_operation_calculation_error(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, Union[int, str]],
        operation_url: str
    ):
        """
        Проверяет обработку случаев, когда предполагается ошибка вычислений.
        Ожидается возвращение кода статуса 1 с сообщением.

        Должен быть переопределен в дочернем классе, т.к. не все операции
        предполагают ошибки в вычислениях.
        """
        response = self.make_request(operation_url, data)
        assert response.status_code == 200
        assert response.json() == expected_result, (
            f"Ожидалось: {expected_result},\n"
            f"получено: {response.json()}"
        )

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 1, },
             {"statusCode": 2,
              "statusMessage": "Не указаны необходимые параметры"}),

            ({"y": 1, },
             {"statusCode": 2,
              "statusMessage": "Не указаны необходимые параметры"}),

            ({},
             {"statusCode": 2,
              "statusMessage": "Не указаны необходимые параметры"}),
        ]
    )
    def test_operation_request_body_missing_keys(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, Union[int, str]],
        operation_url: str
    ):
        """
        Проверяет обработку случаев, когда отсутствуют необходимые ключи тела.
        Ожидается возвращение кода статуса 2 с сообщением.
        """
        response = self.make_request(operation_url, data)
        assert response.status_code == 200
        assert response.json() == expected_result, (
            f"Ожидалось: {expected_result},\n"
            f"получено: {response.json()}"
        )

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 1, "y": "foobar"},
             {"statusCode": 3, "statusMessage":
              "Значения параметров должны быть целыми"}),

            ({"x": "foobar", "y": 1},
             {"statusCode": 3,
              "statusMessage": "Значения параметров должны быть целыми"}),

            ({"x": "foobar", "y": "foobar"},
             {"statusCode": 3,
              "statusMessage": "Значения параметров должны быть целыми"}),

            ({"x": 1, "y": 1.2},
             {"statusCode": 3,
              "statusMessage": "Значения параметров должны быть целыми"}),

            ({"x": 1.2, "y": 1},
             {"statusCode": 3,
              "statusMessage": "Значения параметров должны быть целыми"}),

            ({"x": 1.2, "y": 1.2},
             {"statusCode": 3,
              "statusMessage": "Значения параметров должны быть целыми"}),
        ]
    )
    def test_addition_invalid_value_type(
        self,
        data: Dict[str, Any],
        expected_result: Dict[str, Union[int, str]],
        operation_url: str
    ):
        """
        Проверяет обработку случаев, когда значения тела запроса
        не соответствуют integer.
        Ожидается возвращение кода статуса 3 с сообщением.
        """
        response = self.make_request(operation_url, data)
        assert response.status_code == 200
        assert response.json() == expected_result, (
            f"Ожидалось: {expected_result},\n"
            f"получено: {response.json()}"
        )

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": (INT32_MIN - 1), "y": 1},
             {"statusCode": 4,
             "statusMessage": "Превышены максимальные значения параметров"}),

            ({"x": 1, "y": (INT32_MIN - 1)},
             {"statusCode": 4,
             "statusMessage": "Превышены максимальные значения параметров"}),

            ({"x": (INT32_MAX + 1), "y": 1},
             {"statusCode": 4,
             "statusMessage": "Превышены максимальные значения параметров"}),

            ({"x": 1, "y": (INT32_MAX + 1)},
             {"statusCode": 4,
             "statusMessage": "Превышены максимальные значения параметров"}),
        ]
    )
    def test_operation_value_exceeds_limit(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, Union[int, str]],
        operation_url: str
    ):
        """
        Проверяет обработку случаев, когда значения параметров x или y
        превышают допустимые пределы.
        Ожидается возвращение кода статуса 4 с сообщением.
        """
        print(data)
        response = self.make_request(operation_url, data)
        print(response.json())
        assert response.status_code == 200
        assert response.json() == expected_result, (
            f"Ожидалось: {expected_result},\n"
            f"получено: {response.json()}"
        )

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 1, "y": "foobar"},
             {"statusCode": 5, "statusMessage": "Не допустимый формат json"}),

            ((("x", 1), ("y", 1)),
             {"statusCode": 5, "statusMessage": "Не допустимый формат json"})
        ]
    )
    def test_operation_invalid_request_format(
        self,
        data: Any,
        expected_result: Dict[str, Union[int, str]],
        operation_url: str
    ):
        """
        Проверяет обработку случаев, когда тело запроса имеет неверный формат.
        Ожидается возвращение кода статуса 5 с сообщением.
        """
        response = requests.post(operation_url, data=data)
        assert response.status_code == 200
        assert response.json() == expected_result, (
            f"Ожидалось: {expected_result},\n"
            f"получено: {response.json()}"
        )
