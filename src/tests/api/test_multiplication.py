from typing import Dict

import pytest

from .base import BaseOperationTest
from .constants import INT32_MAX, INT32_MIN


class TestMultiplication(BaseOperationTest):
    """Класс для тестирования операции multiplication"""
    operation = "multiplication"

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 3, "y": 5}, {"statusCode": 0, "result": 15}),
            ({"x": 3, "y": -5}, {"statusCode": 0, "result": -15}),
            ({"x": 5, "y": 3}, {"statusCode": 0, "result": 15}),
            ({"x": -5, "y": 3}, {"statusCode": 0, "result": -15}),
            ({"x": 3, "y": 0}, {"statusCode": 0, "result": 0}),
            ({"x": 0, "y": 3}, {"statusCode": 0, "result": 0}),

            ({"x": INT32_MIN, "y": INT32_MAX},
             {"statusCode": 0, "result": INT32_MAX * INT32_MIN}),

            ({"x": -INT32_MIN, "y": INT32_MAX},
             {"statusCode": 0, "result": (-INT32_MAX) * INT32_MIN}),

            ({"x": INT32_MIN, "y": -INT32_MAX},
             {"statusCode": 0, "result": INT32_MAX * (-INT32_MIN)}),

            ({"x": -INT32_MIN, "y": -INT32_MAX},
             {"statusCode": 0, "result": (-INT32_MAX) * (-INT32_MIN)}),
        ]
    )
    def test_operation_success(
        self,
        data: Dict[str, int],
        expected_result: Dict[str, int],
        operation_url
    ):
        return super().test_operation_success(
            data, expected_result, operation_url
        )
