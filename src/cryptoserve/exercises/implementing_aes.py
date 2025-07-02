import os

from cryptoserve.exercises.primitives import key_addition, mix_columns, sbox, shift_rows
from cryptoserve.messaging import Client
from cryptoserve.types import DataMismatchError


async def implementing_aes(client: Client) -> None:
    byte = os.urandom(1)
    await client.send(byte)
    await client.expect(1, verify_sbox_implementation, original=byte)


def verify_sbox_implementation(received_data: bytes, original: bytes) -> None:
    expected = sbox(original[0])

    if expected != received_data[0]:
        raise DataMismatchError(
            f"received byte {received_data[0]} does not match expected byte {expected}"
        )
