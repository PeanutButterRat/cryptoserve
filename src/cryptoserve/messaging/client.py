import asyncio

HEADER_LENGTH_BYTES = 2


class Client:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer

    async def send(self, data: bytes):
        data_length = len(data)
        header = data_length.to_bytes(HEADER_LENGTH_BYTES)
        entire_message = header + data
        self.writer.write(entire_message)
        await self.writer.drain()

    async def recieve(self) -> bytes:
        header = await self.reader.read(HEADER_LENGTH_BYTES)
        data_length = int.from_bytes(header)
        data = await self.reader.read(data_length)
        return data
