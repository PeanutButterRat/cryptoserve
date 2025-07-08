import asyncio
from functools import partial
from typing import Callable

from cryptoserve.greeting import EXERCISES, GREETING
from cryptoserve.messaging import Client
from cryptoserve.types import ClientTimeoutError, ExerciseError


async def serve(host: str, port: int, timeout: int):
    handler = partial(connect, timeout=timeout)
    server = await asyncio.start_server(handler, host, port)
    address = server.sockets[0].getsockname()

    print(f"Serving on {address}")

    async with server:
        await server.serve_forever()


async def connect(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, timeout: int
):
    address = writer.get_extra_info("peername")

    print(f"Accepted connection from {address}")

    client = Client(reader, writer, timeout=timeout)
    error = None

    try:
        await handle_client(client)
    except ExerciseError as e:
        print(f"An error occurred: {e}")
        error = e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        error = ExerciseError(
            error=f"unexpected server error",
            explanation="Something wrong happened with the server that was unintentional. Please reach out to your instructor to diagnose the issue.",
        )

    if error:
        try:
            message = error.json()
            await client.error(message)
        except:
            pass

    print(f"Terminating connection with {address}")


async def handle_client(client: Client):
    try:
        await client.send(GREETING.encode())
        selection = await client.expect_str()
        selection = clamp(int(selection), 0, len(EXERCISES) - 1)
        exercise = EXERCISES[selection]
        await exercise(client)
    except TimeoutError:
        raise ClientTimeoutError(
            error="the connection timed out",
            explanation=f"You took to long to respond to the server. The server waits at most {client.timeout} second{'s' if client.timeout != 0 else ''} for a response before closing the connection.",
            hints=[
                "Are you formatting your message headers correctly?",
                "Is you message the correct length? The server might be waiting for a longer message."
                "Did you miss any small steps in the exercise?",
            ],
        )


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))
