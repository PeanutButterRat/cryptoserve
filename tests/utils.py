from collections.abc import Callable
from unittest.mock import AsyncMock

import pytest

from cryptoserve.messaging import Client


def wrap_data(data: bytes) -> bytes:
    data_length = len(data)
    header = bytearray(data_length.to_bytes(2))
    return header + data


def create_mock_client(
    received_data: list[bytes | str], sent_data: list[bytes | str] | None
) -> Client:
    received_data = [
        data.encode() if isinstance(data, str) else data for data in received_data
    ]

    forbidden_mock = AsyncMock(
        side_effect=RuntimeError(
            "directly accessing the StreamReader or StreamWriter during a test is not allowed"
        )
    )

    mock_client = Client(forbidden_mock, forbidden_mock)
    mock_client._read = AsyncMock()
    mock_client._write = AsyncMock()
    mock_client.receive = AsyncMock(
        side_effect=[(data, None, None) for data in received_data]
    )
    assertion_index = [0]

    if sent_data is not None:
        sent_data = [
            data.encode() if isinstance(data, str) else data for data in sent_data
        ]

        async def mock_send(
            data: bytes, server_flags: int = 0, exercise_flags: int = 0
        ):
            index = assertion_index[0]
            expected_data = sent_data[index]

            if isinstance(expected_data, list) or isinstance(expected_data, tuple):
                expected_data, expected_server_flags, expected_exercise_flags = (
                    expected_data
                )
                assert (
                    server_flags == expected_server_flags
                ), f"actual server flags 0b{server_flags:b} does not match expected server flags 0b{expected_server_flags:b}"
                assert (
                    exercise_flags == expected_exercise_flags
                ), f"actual exercise flags 0b{exercise_flags:b} does not match expected exercise flags 0b{expected_exercise_flags:b}"

            assert (
                data == expected_data
            ), f"actual data sent ({data}) on call {index} does not match expected data sent ({expected_data})"
            assertion_index[0] += 1

        mock_client.send = mock_send
    else:
        mock_client.send = AsyncMock()

    return mock_client


def run_exercise(
    test_data: list[tuple[list[bytes | str], list[bytes | str] | None]],
) -> Callable:
    def decorator(test: Callable):
        mock_clients = []

        for received_data, sent_data in test_data:
            mock_client = create_mock_client(received_data, sent_data)
            mock_clients.append(mock_client)

        test = pytest.mark.asyncio(test)
        test = pytest.mark.parametrize("client", mock_clients)(test)
        return test

    return decorator
