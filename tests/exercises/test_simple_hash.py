import pytest

from cryptoserve.exercises.simple_hash import *
from tests.utils import simulate_exercise


@simulate_exercise(
    received_data=[b"0" * 256],
)
async def test_initial_length(client):
    with pytest.raises(InvalidLengthError):
        await simple_hash(client)


@simulate_exercise(
    received_data=["123", "123"],
)
async def test_no_padding(client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(client)


@simulate_exercise(
    received_data=["123", "123" + "\x00" * 5],
)
async def test_too_much_padding(client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(client)


@simulate_exercise(received_data=["123", "023\x00"])
async def test_modified_data_during_padding(client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(client)


@simulate_exercise(
    received_data=["Apple", "Apple" + "\x00" * 3, b"\x3a\x58", b"\x7b\xf0"],
)
async def test_incorrect_hash_response(client):
    with pytest.raises(DataMismatchError):
        await simple_hash(client)


@simulate_exercise(
    received_data=["Apple", "Apple" + "\x00" * 3, b"\x3a\x58", b"\x7b\xf1"],
    sent_data=["OK", "OK", b"\x0a\xa0", b"\x62\xae"],
)
async def test_successful_completion(client):
    await simple_hash(client)
