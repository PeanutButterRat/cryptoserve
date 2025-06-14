import asyncio
from typing import Any, Callable, Optional

HEADER_LENGTH_BYTES = 2


class Client:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer

    async def send(self, data: bytes, is_error: bool = False):
        data_length = len(data)
        header = data_length.to_bytes(HEADER_LENGTH_BYTES)

        if is_error:
            header[0] |= (1 << 7)

        entire_message = header + data
        self.writer.write(entire_message)
        await self.writer.drain()

    async def _recieve(self) -> bytes:
        header = await self.reader.read(HEADER_LENGTH_BYTES)
        data_length = int.from_bytes(header)
        data = await self.reader.read(data_length)
        return data

    async def expect(
        self, length: int = -1, verifier: Optional[Callable[[bytes], Any]] = None
    ) -> Any:
        raw_bytes = await self._recieve()

        if length > 0 and len(raw_bytes) != length:
            raise ValueError(
                f"recieved data is not expected length (expected {length} but recieved {len(raw_bytes)})"
            )

        if verifier:
            return verifier(raw_bytes)
        else:
            return raw_bytes

    async def expectstr(self, length: int = -1):
        string = await self.expect(verifier=lambda bytes: bytes.decode())

        if length > 0 and len(string) != length:
            raise ValueError("recived string is not expected length")

        return string

    async def error(self, message: str):
        raw_bytes = message.encode()
        self.send(raw_bytes, True)
