import os

from cryptoserve.messaging import Client
from cryptoserve.types import DataMismatchError

import aes


def sbox(x: int, inverse: bool = False) -> int:
    return aes.core.sbox(x) if not inverse else aes.core.rsbox(x)


def shift_rows(state: bytes, inverse: bool = False) -> bytes:
    return aes.core.shiftrows(state) if not inverse else aes.core.inv_shiftrows(state)


def mix_columns(state: bytes, inverse: bool = False) -> bytes:
    return aes.core.mixcolumns(state) if not inverse else aes.core.inv_mixcolumns(state)


def sub_bytes(state: bytes, inverse: bool = False) -> bytes:
    return aes.core.subbytes(state) if not inverse else aes.core.inv_mixcolumns(state)


def key_addition(state: bytes) -> bytes:
    return aes.core.addroundkey(state)



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
