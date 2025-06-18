from cryptoserve.exercises import ExerciseError
from cryptoserve.messaging import Client
from cryptoserve.types import from_bytes, to_bytes, uint16


async def simple_hash(client: Client):
    data = await client.expect(verifier=validate_initial_data)
    await client.ok()

    chunks = await client.expect(verifier=lambda new: validate_padded_data(new, data))
    await client.ok()

    hash = bytearray([len(data), len(data)])
    hash = from_bytes(hash)

    for i, chunk in enumerate(chunks):
        if i % 2 == 0:
            hash = f(hash, chunk)
            hash = await client.expect(
                2, verifier=lambda data: validate_hash(data, hash)
            )
        else:
            hash = g(hash, chunk)
            await client.send(to_bytes(hash))


def f(a: uint16, b: uint16):
    a ^= b + 0xC0DE
    return (a << 3) | (a >> 13)


def g(a: uint16, b: uint16):
    a ^= b + 0xBEAD
    return a >> 1


def validate_initial_data(data: bytes) -> bytes:
    if not len(data) <= 255:
        raise ExerciseError(
            error="input data is too large",
            explanation="The data you sent was too large in size for SimpleHash.",
            hints=["Are you sending less than 256 bytes of input data?"],
        )

    return data


def validate_padded_data(
    data: bytes, received: bytes
) -> tuple[list[tuple[bytes]], int]:
    padding_error = ExerciseError(
        error="intial data has invalid padding",
        explanation="The initial data has too much padding. The data must be padded with null bytes so that it can be split into even chunks for hashing.",
        hints=[
            "Is the data length a multiple of 4?",
            "If not, are you adding null (0x00) bytes to the end?",
            "Are null bytes only at the end of the data?",
            "Is there",
        ],
    )

    if data.find(received) != 0:
        raise padding_error

    padding = 4 - len(received) % 4
    for byte in data[-padding:]:
        if byte != 0x00:
            raise padding_error

    chunks = list(from_bytes(chunk) for chunk in zip(data[::2], data[1::2]))

    return chunks


def validate_hash(data: bytes, hash: uint16) -> uint16:
    recieved_hash = from_bytes(data)

    if recieved_hash != hash:
        raise ExerciseError(
            error="recived hash does not match expected hash",
            explanation="You made a mistake in hash",
            hints=[
                "Are you applying the operations in the correct order as outlined in the documentation?",
                "Are you using f to hash the data on your turn?",
                "Are you using unsigned 16-bit integers for storing data? Are they being promoted to larger types accidentally?",
            ],
        )
    return hash
