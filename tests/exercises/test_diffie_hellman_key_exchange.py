import pytest

from cryptoserve.exercises.diffie_hellman_key_exchange import (
    diffie_hellman_key_exchange,
)
from cryptoserve.messaging import Client
from cryptoserve.types import DataMismatchError
from tests.utils import simulate_exercise

deterministic_patches = {
    "os.urandom": lambda n: b"\x00" * n,
    "random.randint": lambda *_: 2,
    "random.choice": lambda iterable: iterable[0],
}


@simulate_exercise(
    received_data=[bytes([216]), bytes([1] * 16)],
    patches=deterministic_patches,
)
async def test_plaintext_mismatch(client: Client):
    with pytest.raises(DataMismatchError):
        await diffie_hellman_key_exchange(client)


@simulate_exercise(
    sent_data=[
        bytes([6, 36]),
        b"S/\xde\x11W\xd9Q\xcd\xd3&\xcbU\x872\x03\xbc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    ],
    received_data=[bytes([216]), bytes([0] * 16)],
    patches=deterministic_patches,
)
async def test_successful_completion(client: Client):
    await diffie_hellman_key_exchange(client)
