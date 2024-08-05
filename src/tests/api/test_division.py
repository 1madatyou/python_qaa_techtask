from typing import Dict, Union
import pytest

from .base import BaseOperationTest
from .constants import INT32_MAX, INT32_MIN


class TestDivision(BaseOperationTest):
    """Класс для тестирования операции division"""
    operation = "division"

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 15, "y": 5}, {"statusCode": 0, "result": 3}),
            ({"x": 3, "y": 15}, {"statusCode": 0, "result": 0}),
            ({"x": -15, "y": 3}, {"statusCode": 0, "result": -5}),
            ({"x": 15, "y": -3}, {"statusCode": 0, "result": -5}),
            ({"x": -15, "y": -3}, {"statusCode": 0, "result": 5}),
            ({"x": 0, "y": 3}, {"statusCode": 0, "result": 0}),

            ({"x": INT32_MAX, "y": INT32_MAX},
             {"statusCode": 0, "result": INT32_MAX//INT32_MAX}),
            ({"x": INT32_MIN, "y": INT32_MIN},
             {"statusCode": 0, "result": INT32_MIN//INT32_MIN}),
        ]
    )
    def test_operation_success(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, int],
        operation_url: str
    ):
        return super().test_operation_success(
            data, expected_result, operation_url
        )

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 3, "y": 0},
             {"statusCode": 1, "statusMessage": "Ошибка вычисления"}),

            ({"x": -3, "y": 0},
             {"statusCode": 1, "statusMessage": "Ошибка вычисления"}),

            ({"x": 0, "y": 0},
             {"statusCode": 1, "statusMessage": "Ошибка вычисления"}),

        ]
    )
    def test_operation_calculation_error(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, Union[str, int]],
        operation_url: str
    ):
        return super().test_operation_calculation_error(
            data, expected_result, operation_url
        )
