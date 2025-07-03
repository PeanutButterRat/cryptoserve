import os
import random

import aes

from cryptoserve.messaging import Client
from cryptoserve.types import DataMismatchError


def sbox(x: int, inverse: bool = False) -> int:
    return aes.core.sbox(x) if not inverse else aes.core.rsbox(x)


def shift_rows(state: bytes, inverse: bool = False) -> bytes:
    state = (
        aes.core.mixcolumns(state) if not inverse else aes.core.inv_mixcolumns(state)
    )
    return bytes(state)


def mix_columns(state: bytes, inverse: bool = False) -> bytes:
    state = (
        aes.core.mixcolumns(state) if not inverse else aes.core.inv_mixcolumns(state)
    )
    return bytes(state)


def sub_bytes(state: bytes, inverse: bool = False) -> bytes:
    state = aes.core.subbytes(state) if not inverse else aes.core.inv_mixcolumns(state)
    return bytes(state)


def key_addition(state: bytes, round_key: bytes) -> bytes:
    key = aes.core.addroundkey(list(state), list(round_key))
    return bytes(key)


def get_random_repetitions():
    return random.randint(2, 5)


async def implementing_aes(client: Client) -> None:
    for _ in range(get_random_repetitions()):
        keys = os.urandom(32)
        await client.send(keys, exercise_flags=0)
        await client.expect(16, verify_key_addition_implementation, keys=keys)

    for _ in range(get_random_repetitions()):
        byte = os.urandom(1)
        await client.send(byte, exercise_flags=1)
        await client.expect(1, verify_sbox_implementation, original=byte)

    for _ in range(get_random_repetitions()):
        bytes = os.urandom(16)
        await client.send(bytes, exercise_flags=2)
        await client.expect(16, verify_sub_bytes_implementation, original=bytes)

    for _ in range(get_random_repetitions()):
        bytes = os.urandom(16)
        await client.send(bytes, exercise_flags=3)
        await client.expect(16, verify_shift_rows_implementation, original=bytes)

    for _ in range(get_random_repetitions()):
        bytes = os.urandom(16)
        await client.send(bytes, exercise_flags=4)
        await client.expect(16, verify_mix_columns_implementation, original=bytes)


def verify_sbox_implementation(received_data: bytes, original: bytes) -> None:
    expected = sbox(original[0])

    if expected != received_data[0]:
        raise DataMismatchError(
            f"received byte {received_data[0]} does not match expected byte {expected}"
        )


def verify_sub_bytes_implementation(received_data: bytes, original: bytes) -> None:
    expected = sub_bytes(original)

    if expected != received_data:
        raise DataMismatchError(
            f"received bytes {received_data} does not match expected bytes {expected}"
        )


def verify_shift_rows_implementation(received_data: bytes, original: bytes) -> None:
    expected = shift_rows(original)

    if expected != received_data:
        raise DataMismatchError(
            f"received bytes {received_data} does not match expected bytes {expected}"
        )


def verify_key_addition_implementation(received_data: bytes, keys: bytes) -> None:
    state, keys = keys[:16], keys[16:]
    expected = key_addition(state, keys)

    if expected != received_data:
        raise DataMismatchError(
            f"received bytes {received_data} does not match expected bytes {expected}"
        )


def verify_mix_columns_implementation(received_data: bytes, original: bytes) -> None:
    expected = mix_columns(original)

    if expected != received_data:
        raise DataMismatchError(
            f"received bytes {received_data} does not match expected bytes {expected}"
        )
