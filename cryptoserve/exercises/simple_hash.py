import numpy as np

from cryptoserve.messaging import Client


async def simple_hash(client: Client):
    while data := (await client.recieve()):
        hash, chunk = data[:2], data[2:]
        hash = np.uint16(int.from_bytes(hash))
        chunk = np.uint16(int.from_bytes(chunk))
        hash = g(hash, chunk)
        await client.send(int(hash).to_bytes(2))


def g(a: np.uint16, b: np.uint16):
    a ^= b + 0xBEAD
    return a >> 1
