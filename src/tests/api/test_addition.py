from typing import Dict
import pytest

from .base import BaseOperationTest
from .constants import INT32_MIN, INT32_MAX


class TestAddition(BaseOperationTest):
    """Класс для тестирования операции addition"""
    operation = "addition"

    @pytest.mark.parametrize(
        "data, expected_result",
        [
            ({"x": 3, "y": 5}, {"statusCode": 0, "result": 8}),
            ({"x": 3, "y": -5}, {"statusCode": 0, "result": -2}),
            ({"x": 5, "y": 3}, {"statusCode": 0, "result": 8}),
            ({"x": -5, "y": 3}, {"statusCode": 0, "result": -2}),
            ({"x": 3, "y": 0}, {"statusCode": 0, "result": 3}),
            ({"x": 0, "y": 3}, {"statusCode": 0, "result": 3}),

            ({"x": INT32_MAX, "y": INT32_MAX},
             {"statusCode": 0, "result": INT32_MAX+INT32_MAX}),
            ({"x": INT32_MIN, "y": INT32_MIN},
             {"statusCode": 0, "result": INT32_MIN+INT32_MIN}),
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
