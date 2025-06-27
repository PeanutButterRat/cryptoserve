from collections.abc import Callable
from unittest.mock import AsyncMock

import pytest

from cryptoserve.messaging import Client


def create_mock_client(recieved_data: list[bytes]):
    forbidden_mock = AsyncMock(
        side_effect=RuntimeError(
            "directly accessing the StreamReader or StreamWriter during a test is not allowed"
        )
    )
    mock_client = Client(forbidden_mock, forbidden_mock)
    mock_client._recieve = AsyncMock(side_effect=recieved_data)
    mock_client._send = AsyncMock()

    return mock_client


def run_exercise(recieved_data: list[list[bytes]]):
    def decorator(test: Callable):
        test = pytest.mark.asyncio(test)
        test = pytest.mark.parametrize(
            "client", [create_mock_client(data) for data in recieved_data]
        )(test)
        return test

    return decorator
