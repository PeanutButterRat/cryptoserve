import asyncio

HOST = "127.0.0.1"
PORT = 5050


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    address = server.sockets[0].getsockname()

    print(f"Serving on {address}")

    async with server:
        await server.serve_forever()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    address = writer.get_extra_info("peername")

    data = await reader.readline()
    message = data.decode()
    print(f"{address}: {message}")

    writer.write(b"Pong")
    await writer.drain()


if __name__ == "__main__":
    asyncio.run(main())
