import argparse
import asyncio

import numpy as np

from .network import Client

np.seterr(over="ignore")


class ArgparseFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.MetavarTypeHelpFormatter
):
    pass


def main():
    argparser = argparse.ArgumentParser(
        prog="Cryptoserve",
        description="Server software that houses a library of cryptography-related learning exercises.",
        formatter_class=ArgparseFormatter,
    )
    argparser.add_argument(
        "--host", type=str, default="127.0.0.1", help="host address to bind to"
    )

    argparser.add_argument(
        "--port", "-p", type=int, default=5050, help="port number to bind to"
    )

    args = argparser.parse_args()

    if not (0 <= args.port <= 65535):
        argparser.error("port must be in range 0-65535")

    asyncio.run(serve(args.host, args.port))


async def serve(host: str, port: int):
    server = await asyncio.start_server(handle_client, host, port)
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

    client = Client(reader, writer)
    await client.send(greeting.encode())
    selection = await client.recieve()
    selection = selection.decode()
    selection = clamp(int(selection), 0, len(EXERCISES) - 1)
    exercise = EXERCISES[selection]
    await exercise[1](client)

    print(f"Terminating connection with {address}")


async def simple_hash(client: Client):
    while data := (await client.recieve()):
        hash, chunk = data[:2], data[2:]
        hash = np.uint16(int.from_bytes(hash))
        chunk = np.uint16(int.from_bytes(chunk))
        hash = g(hash, chunk)
        await client.send(int(hash).to_bytes(2))


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
