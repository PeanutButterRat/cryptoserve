from cryptoserve.exercises import (
    DataMismatchError,
    InvalidLengthError,
    InvalidPaddingError,
)
from cryptoserve.messaging import Client
from cryptoserve.types import from_bytes, to_bytes, uint16


async def simple_hash(client: Client):
    data = await client.expect(verifier=vertify_initial_data)
    await client.ok()

    chunks = await client.expect(verifier=verify_padded_data, initial_data=data)
    await client.ok()

    hash = bytearray([len(data), len(data)])
    hash = from_bytes(hash)

    for i, chunk in enumerate(chunks):
        if i % 2 == 0:
            hash = f(hash, chunk)
            hash = await client.expect(2, verify_hash, hash=hash)
        else:
            hash = g(hash, chunk)
            await client.send(to_bytes(hash))


def f(a: uint16, b: uint16):
    a ^= b + 0xC0DE
    return (a << 3) | (a >> 13)


def g(a: uint16, b: uint16):
    a ^= b + 0xBEAD
    return a >> 1


def vertify_initial_data(data: bytes) -> bytes:
    if not len(data) <= 255:
        raise InvalidLengthError(
            error="input data is too large",
            explanation="The data you sent was too large in size for Simple Hash to handle. Recall that the length must be representable by a single byte.",
            hints=["Are you sending less than 256 bytes of input data?"],
        )

    return data


def verify_padded_data(
    padded_data: bytes, initial_data: bytes
) -> tuple[list[tuple[bytes]], int]:

    padding_amount = 4 - len(initial_data) % 4

    if len(padded_data) != len(initial_data) + padding_amount:
        raise InvalidPaddingError(
            explanation="The padded data has the wrong amount of padding.",
            hints=[
                "Is the data padded to the next multiple of 4?",
            ],
        )

    if padded_data.find(initial_data) != 0 or not all(
        byte == 0x00 for byte in padded_data[-padding_amount:]
    ):
        raise InvalidPaddingError(
            explanation="The original data was padded improperly.",
            hints=[
                "Is padding applied only to the end of the data to be hashed?",
                "Are you padding the data with null (0x00) bytes?",
                "Make sure the original data is not modified after being sent (besides padding, of course).",
            ],
        )

    chunks = list(
        from_bytes(chunk) for chunk in zip(padded_data[::2], padded_data[1::2])
    )

    return chunks


def verify_hash(data: bytes, hash: uint16) -> uint16:
    recieved_hash = from_bytes(data)

    if recieved_hash != hash:
        raise DataMismatchError(
            data_type="hash",
            explanation="You made some mistake in hashing.",
            hints=[
                "Are you applying the operations in the correct order as outlined in the documentation?",
                "Are you using f to hash the data on your turn (not g)?",
                "Are you using unsigned 16-bit integers for storing data? Are they being promoted to larger types accidentally?",
                "Are you sending the data in the correct order?",
            ],
        )
    return hash
