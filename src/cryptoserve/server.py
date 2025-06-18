import asyncio
from typing import Callable

from cryptoserve.greeting import EXERCISES, GREETING
from cryptoserve.messaging import Client
from cryptoserve.types.errors import ExerciseError


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

    selection = await client.expect_str()
    selection = clamp(int(selection), 0, len(EXERCISES) - 1)
    exercise = EXERCISES[selection]

    await run_exercise(client, exercise)

    print(f"Terminating connection with {address}")


async def run_exercise(client: Client, exercise: Callable[[Client], None]):
    try:
        await exercise(client)
    except ExerciseError as error:
        print(f"An error occurred: {error}")
        message = error.json()
        await client.error(message)


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))
