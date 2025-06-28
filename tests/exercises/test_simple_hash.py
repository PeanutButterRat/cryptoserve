import pytest

from cryptoserve.exercises.simple_hash import *
from tests.utils import run_exercise


@run_exercise([[b"0" * 256], [b"0" * 500]])
async def test_initial_length(client):
    with pytest.raises(InvalidLengthError):
        await simple_hash(client)


@run_exercise(
    [
        ["123", "123"],
        ["123", "123\x01"],
        ["123", "023\x00"],
        ["1234", "1234" + "\x00" * 3],
        ["123", "123" + "\x00" * 5],
    ]
)
async def test_invalid_padding(client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(client)


@run_exercise(
    [
        ["Apple", "Apple" + "\x00" * 3, b"\x00\x00"],
        ["Apple", "Apple" + "\x00" * 3, b"\x3a\x59"],
        ["Apple", "Apple" + "\x00" * 3, b"\x3a\x58", b"\x7b\xf0"],
    ]
)
async def test_invalid_hash(client):
    with pytest.raises(DataMismatchError):
        await simple_hash(client)


@run_exercise(
    [
        ["Apple", "Apple" + "\x00" * 3, b"\x3a\x58", b"\x7b\xf1"],
    ]
)
async def test_successful_completion(client):
    await simple_hash(client)
