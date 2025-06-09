import argparse
import asyncio

import numpy as np

from cryptoserve.greeting import EXERCISES, GREETING
from cryptoserve.messaging import Client

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

    client = Client(reader, writer)
    await client.send(GREETING.encode())

    selection = await client.recieve()
    selection = selection.decode()
    selection = clamp(int(selection), 0, len(EXERCISES) - 1)
    exercise = EXERCISES[selection]

    await exercise(client)

    print(f"Terminating connection with {address}")


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


if __name__ == "__main__":
    asyncio.run(main())
