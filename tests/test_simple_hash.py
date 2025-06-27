import asyncio
from unittest.mock import AsyncMock

import pytest

from cryptoserve.exercises.simple_hash import simple_hash
from cryptoserve.messaging import Client
from cryptoserve.types import InvalidPaddingError


@pytest.fixture
def mock_client(request):
    mock_reader = AsyncMock(spec=asyncio.StreamReader)
    mock_writer = AsyncMock(spec=asyncio.StreamWriter)
    mock_client = Client(mock_reader, mock_writer)

    sent_data, recieved_data = request.param
    mock_client._recieve = AsyncMock(side_effect=recieved_data)
    mock_client._send = AsyncMock(side_effect=sent_data)

    return mock_client


@pytest.mark.parametrize(
    ["mock_client"],
    [
        [[[b"abc", b"abc"], None]],
    ],
    indirect=["mock_client"],
)
@pytest.mark.asyncio
async def test_simple_hash_invalid_padding(mock_client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(mock_client)
