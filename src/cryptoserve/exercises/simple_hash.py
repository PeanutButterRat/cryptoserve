from cryptoserve.messaging import Client
from cryptoserve.types import from_bytes, to_bytes, uint16


async def simple_hash(client: Client):
    data_length = from_bytes(await client.expect())

    for _ in range(data_length // 2):
        data = await client.expect()
        hash, chunk = data[:2], data[2:]
        hash = from_bytes(hash)
        chunk = from_bytes(chunk)
        hash = g(hash, chunk)
        response = to_bytes(hash)
        await client.send(response)


def g(a: uint16, b: uint16):
    a ^= b + 0xBEAD
    return a >> 1
