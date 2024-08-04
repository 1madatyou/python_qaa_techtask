from typing import Dict
import pytest

from .base import BaseOperationTest
from .constants import INT32_MIN, INT32_MAX

class TestRemainder(BaseOperationTest):
    """Класс для тестирования операции remainder"""
    operation = "remainder"

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 3, "y": 5}, {"statusCode": 0, "result": 3%5}),
            ({"x": 3, "y": -5}, {"statusCode": 0, "result": 3%-5}),
            ({"x": 5, "y": 3}, {"statusCode": 0, "result": 5%3}),
            ({"x": -5, "y": 3}, {"statusCode": 0, "result": -5%3}),

            ({"x": 0, "y": 3}, {"statusCode": 0, "result": 0%3}),

            ({"x": INT32_MAX, "y": INT32_MAX}, 
             {"statusCode": 0, "result": INT32_MAX%INT32_MAX}),
            ({"x": INT32_MIN, "y": INT32_MIN}, 
             {"statusCode": 0, "result": INT32_MIN%INT32_MIN}),
        ]
    )
    def test_operation_success(self, data: Dict[str, int], expected_result, operation_url):
        return super().test_operation_success(data, expected_result, operation_url)
    

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 3, "y": 0}, {"statusCode": 1, "statusMessage": "Ошибка вычисления"}),
            ({"x": -3, "y": 0}, {"statusCode": 1, "statusMessage": "Ошибка вычисления"}),
            ({"x": 0, "y": 0}, {"statusCode": 1, "statusMessage": "Ошибка вычисления"}),
        ]
    )
    def test_operation_calculation_error(self, data, expected_result, operation_url):
        return super().test_operation_calculation_error(data, expected_result, operation_url)