from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock

import pytest

from cryptoserve.messaging import Client


class MockClient(Client):
    def __init__(self, received_data, sent_data):
        forbidden_mock = AsyncMock(
            side_effect=RuntimeError(
                "directly accessing the StreamReader or StreamWriter during a test is not allowed"
            )
        )

        super().__init__(forbidden_mock, forbidden_mock)
        self._read = AsyncMock()
        self._write = AsyncMock()

        self.received_data = self._convert_messages_to_proper_tuples(
            received_data, default_value=0
        )
        self.received_call_index = 0

        if sent_data is None:
            self.send = AsyncMock()
        else:
            self.sent_data = self._convert_messages_to_proper_tuples(
                sent_data, default_value=None
            )
            self.sent_call_index = 0

    def _convert_messages_to_proper_tuples(
        self, messages: list[tuple | str | bytes], default_value: Any = None
    ):
        tuples = []

        for message in messages:
            if isinstance(message, tuple):
                data, server_flags, exercise_flags = message
            else:
                data, server_flags, exercise_flags = (
                    message,
                    default_value,
                    default_value,
                )

            if isinstance(data, str):
                data = data.encode()

            tuples.append((data, server_flags, exercise_flags))

        return tuples

    async def send(self, data: bytes, server_flags: int = 0, exercise_flags: int = 0):
        if self.sent_call_index >= len(self.sent_data):
            raise RuntimeError("ran out of sent data to verify")

        expected_data, expected_server_flags, expected_exercise_flags = self.sent_data[
            self.sent_call_index
        ]

        if expected_data is not None:
            assert (
                data == expected_data
            ), f"actual data sent ({data}) on call {self.sent_call_index} does not match expected data sent ({expected_data})"

        if expected_server_flags is not None:
            assert (
                server_flags == expected_server_flags
            ), f"actual server flags 0b{server_flags:b} does not match expected server flags 0b{expected_server_flags:b}"

        if expected_exercise_flags is not None:
            assert (
                exercise_flags == expected_exercise_flags
            ), f"actual exercise flags 0b{exercise_flags:b} does not match expected exercise flags 0b{expected_exercise_flags:b}"

        self.sent_call_index += 1

    async def receive(self):
        if self.received_call_index >= len(self.received_data):
            raise RuntimeError("ran out of received data to verify")

        test_data = self.received_data[self.received_call_index]
        self.received_call_index += 1

        return test_data


def simulate_exercise(
    received_data: list[bytes | str], sent_data: list[bytes | str] = None
) -> Callable:
    def decorator(test: Callable):
        client = MockClient(received_data, sent_data)
        test = pytest.mark.asyncio(test)
        test = pytest.mark.parametrize("client", [client])(test)
        return test

    return decorator
