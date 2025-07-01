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
    mock_client._receive = AsyncMock(side_effect=received_data)
    assertion_index = [0]

    if sent_data is not None:
        sent_data = [
            data.encode() if isinstance(data, str) else data for data in sent_data
        ]
        sent_data = [wrap_data(data) for data in sent_data]

        async def mock_send(data: bytes):
            index = assertion_index[0]
            expected = sent_data[index]
            assert (
                data == expected
            ), f"actual data sent on call {index} ({data}) does not match expected data sent ({expected})"
            assertion_index[0] += 1

        mock_client._send = mock_send
    else:
        mock_client._send = AsyncMock()

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
