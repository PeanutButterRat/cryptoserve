from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock

import pytest

from cryptoserve.messaging import Client


class MockClient(Client):
    def __init__(
        self,
        received_data: list[tuple | str | bytes],
        sent_data: list[tuple | str | bytes | None] = None,
    ):
        """A mocked client for testing purposes.

        Args:
            received_data: Data to return on regular calls to receive().
            sent_data: Data to compare against regular calls to send().
        """
        forbidden_mock = AsyncMock(
            side_effect=RuntimeError(
                "directly accessing the StreamReader or StreamWriter during a test is not allowed"
            )
        )

        super().__init__(forbidden_mock, forbidden_mock)
        self._read = AsyncMock()
        self._write = AsyncMock()

        self.received_data = MockClient._convert_messages_to_proper_tuples(
            received_data, default_value=0
        )
        self.received_call_index = 0

        if sent_data is None:
            self.send = AsyncMock()
        else:
            self.sent_data = MockClient._convert_messages_to_proper_tuples(
                sent_data, default_value=None
            )
            self.sent_call_index = 0

    @classmethod
    def _convert_messages_to_proper_tuples(
        cls, messages: list[tuple | str | bytes | None], default_value: Any = None
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

    async def send(
        self, data: bytes | str, server_flags: int = 0, exercise_flags: int = 0
    ):
        if isinstance(data, str):
            data = data.encode()

        if self.sent_call_index >= len(self.sent_data):
            raise RuntimeError("ran out of sent data to verify")

        expected_data, expected_server_flags, expected_exercise_flags = self.sent_data[
            self.sent_call_index
        ]

        if expected_data is not None:
            assert (
                data == expected_data
            ), f"actual data sent ({data}) sent on call {self.sent_call_index} does not match expected data sent ({expected_data})"

        if expected_server_flags is not None:
            assert (
                server_flags == expected_server_flags
            ), f"actual server flags (0b{server_flags:b}) sent on call {self.sent_call_index} does not match expected server flags (0b{expected_server_flags:b})"

        if expected_exercise_flags is not None:
            assert (
                exercise_flags == expected_exercise_flags
            ), f"actual exercise flags (0b{exercise_flags:b}) sent on call {self.sent_call_index} does not match expected exercise flags (0b{expected_exercise_flags:b})"

        self.sent_call_index += 1

    async def receive(self):
        if self.received_call_index >= len(self.received_data):
            raise RuntimeError("ran out of received data to verify")

        test_data = self.received_data[self.received_call_index]
        self.received_call_index += 1

        return test_data


def simulate_exercise(
    received_data: list[tuple | bytes | str],
    sent_data: list[tuple | bytes | str] = None,
) -> Callable:
    """Decorator that sets up a Pytest function for simulating a networked exercise.

    Use this decorator to simulate an exercise by bypassing traditional sockets and injecting
    test data directly into a mocked client. It allows testing of client behavior without requiring
    actual network communication.

    Each argument can be given as a list of bytes (bytes to send/receive per call) or strings. Strings
    are automatically encoded using UTF-8 and treated the same as bytes. Alternatively, you can specify
    a tuple in the form (str | bytes, int | None, int | None). The first item is the data to send or receive,
    and the second and third are the server and exercise flags, respectively. Any of these values can be
    None, in which case they are ignored during validation.

    If `sent_data` is None, no validation is performed on what the client sends. This can also be None
    for individual elements in the `sent_data` list, meaning the corresponding call will not be checked.
    Similarly, any flag field (server or exercise) can be None to skip validation for that flag.

    Args:
        received_data: A list of data elements the mock client will receive.
            This simulates incoming messages from the server. Each subsequent call returns the next
            value in the list, corresponding to a sequence of `Client.receive()` calls.

        sent_data: A list of expected data that the client is
            supposed to send during the exercise. Used for validating outbound communication.
            If None, no validation is performed on outbound data.

    Returns:
        Callable: A decorated async Pytest test function with a mocked client injected as a parameter.

    Examples:

        ::

            # Returns "hello".encode() on next call to receive() and checks if
            # "world".encode() is sent on next call to send(). All flags are ignored.
            @simulate_exercise(received_data=["hello"], sent_data=["world"])
            async def test_echo(client):
                await exercise(client)

        ::

            # Same as example above, but no encoding is performed. b"data1" and b"data2" are received as is.
            # Calls to send() are ignored.
            @simulate_exercise(received_data=[b"data1", b"data2"])
            async def test_unchecked_send(client):
                await exercise(client)

        ::

            # Regular strings are encoded as UTF-8, and the appropriate flags are returned in the calls
            # to receive(). The server flags are ignored for correctness in the last call to client.send().
            @simulate_exercise(
                received_data=[
                    ("welcome", 0b001, 0b010),
                    ("next", 0b000, 0b011)
                ],
                sent_data=[
                    ("ack", 0b100, None),  # Only data and exercise flags are checked for correctness (server flags ignored).
                    None  # No validation for this call
                ]
            )
            async def test_with_flags(client):
                await exercise(client)
    """

    def decorator(test: Callable):
        client = MockClient(received_data, sent_data)
        test = pytest.mark.asyncio(test)
        test = pytest.mark.parametrize("client", [client])(test)
        return test

    return decorator
