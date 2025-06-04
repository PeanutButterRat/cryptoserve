import asyncio

import numpy as np

HOST = "127.0.0.1"
PORT = 5050

np.seterr(over="ignore")


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    address = server.sockets[0].getsockname()

    print(f"Serving on {address}")

    async with server:
        await server.serve_forever()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    address = writer.get_extra_info("peername")

    print(f"Accepted connection from {address}")

    greeting = [
        "=======================",
        "Welcome to Cryptoserve!",
        "=======================",
        "",
        "Available Exercises:",
    ]

    for i, (name, _) in enumerate(EXERCISES):
        greeting.append(f"  {i}. {name}")

    greeting = "\n".join(greeting)

    await send(greeting.encode(), writer)
    selection = await recieve(reader)
    selection = selection.decode()
    selection = clamp(int(selection), 0, len(EXERCISES))
    exercise = EXERCISES[selection]
    await exercise[1](reader, writer)

    print(f"Terminating connection with {address}")


async def send(data: bytes, writer: asyncio.StreamWriter):
    data_length = len(data)
    raw_bytes = data_length.to_bytes(2) + data
    writer.write(raw_bytes)
    await writer.drain()


async def recieve(reader: asyncio.StreamReader):
    header = await reader.read(2)
    data_length = int.from_bytes(header)
    data = await reader.read(data_length)
    return data


async def simple_hash(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while data := (await recieve(reader)):
        hash, chunk = data[:2], data[2:]
        hash = np.uint16(int.from_bytes(hash))
        chunk = np.uint16(int.from_bytes(chunk))
        hash = g(hash, chunk)
        await send(int(hash).to_bytes(2), writer)


def f(a: np.uint16, b: np.uint16):
    a ^= b + 0xC0DE
    return (a << 3) | (a >> 13)


def g(a: np.uint16, b: np.uint16):
    a ^= b + 0xBEAD
    return a >> 1


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


EXERCISES = [("Simple Hash", simple_hash)]


if __name__ == "__main__":
    asyncio.run(main())
