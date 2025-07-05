from unittest.mock import AsyncMock

import pytest

from tests.utils import MockClient


@pytest.mark.parametrize(
    "messages, expected",
    [
        (["a", "b", "c"], [(b"a", None, None), (b"b", None, None), (b"c", None, None)]),
        (
            [b"a", "b", b"c"],
            [(b"a", None, None), (b"b", None, None), (b"c", None, None)],
        ),
        ([None, "a", "c"], [(None, None, None), (b"a", None, None)]),
        ([("a", 1, 2), ("b", 0, None)], [(b"a", 1, 2), (b"b", 0, None)]),
    ],
)
def test_tuple_conversion(messages, expected):
    tuples = MockClient._convert_messages_to_proper_tuples(messages)

    for actual, expected in zip(tuples, expected):
        assert actual == expected


def test_mock_client_creation():
    client = MockClient([], None)
    assert isinstance(client.send, AsyncMock)


@pytest.mark.asyncio
async def test_mock_client_receive():
    client = MockClient(["a", ("b", 1, 2), (b"c", None, None)])

    assert await client.receive() == (b"a", 0, 0)
    assert await client.receive() == (b"b", 1, 2)
    assert await client.receive() == (b"c", None, None)

    with pytest.raises(RuntimeError):
        await client.receive()


@pytest.mark.asyncio
async def test_mock_client_send():
    client = MockClient([], [None, ("b", 1, 2), None])

    await client.send("ignored")

    with pytest.raises(AssertionError):
        await client.send(b"b", 1, 3)

    await client.send(b"b", 1, 2)
    await client.send("ignored", 1, 2)

    with pytest.raises(RuntimeError):
        await client.send("nothing")
