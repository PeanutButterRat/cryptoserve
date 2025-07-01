import pytest

from cryptoserve.exercises.simple_hash import *
from tests.utils import run_exercise


@run_exercise(
    [
        ([b"0" * 256], None),
        ([b"0" * 500], None),
    ]
)
async def test_initial_length(client):
    with pytest.raises(InvalidLengthError):
        await simple_hash(client)


@run_exercise(
    [
        (["123", "123"], None),
        (["123", "123\x01"], None),
        (["123", "023\x00"], None),
        (["1234", "1234" + "\x00" * 3], None),
        (["123", "123" + "\x00" * 5], None),
    ]
)
async def test_invalid_padding(client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(client)


@run_exercise(
    [
        (["Apple", "Apple" + "\x00" * 3, b"\x00\x00"], None),
        (["Apple", "Apple" + "\x00" * 3, b"\x3a\x59"], None),
        (["Apple", "Apple" + "\x00" * 3, b"\x3a\x58", b"\x7b\xf0"], None),
    ]
)
async def test_invalid_hash(client):
    with pytest.raises(DataMismatchError):
        await simple_hash(client)


@run_exercise(
    [
        (
            ["Apple", "Apple" + "\x00" * 3, b"\x3a\x58", b"\x7b\xf1"],
            ["OK", "OK", b"\x0a\xa0", b"\x62\xae"],
        ),
    ]
)
async def test_successful_completion(client):
    await simple_hash(client)
