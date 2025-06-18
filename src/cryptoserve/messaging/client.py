import asyncio
from typing import Any, Callable, Optional

HEADER_LENGTH_BYTES = 2


class Client:
    """
    This class is used as an interface for sending and recieving data from a socket between the client and server.
    It provides various utilities to abstract the underlying protocol information to send blobs of data back and
    forth in an asynchronous manner.
    """

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Constructor method.

        Args:
            reader: Reader instance for reading from the socket. This should not be instantiated directly but rather
                come from the call to **asyncio.start_server**.
                See `asynchio.StreamWriter <https://docs.python.org/3/library/asyncio-stream.html#streamreader>`_.
            writer: Writer instance for writing to the socket. This also should come from **asyncio.start_server**.
                See `asynchio.StreamReader <https://docs.python.org/3/library/asyncio-stream.html#streamreader>`_.
        """
        self.reader = reader
        self.writer = writer

    async def send(self, data: bytes, is_error: bool = False):
        """
        Send a collection of bytes to the client.

        Args:
            data: The bytes to send.
            is_error: Whether the message should set the error flag. Defaults to False.
        """
        data_length = len(data)
        header = bytearray(data_length.to_bytes(HEADER_LENGTH_BYTES))

        if is_error:
            header[0] |= 1 << 7

        entire_message = header + data
        self.writer.write(entire_message)
        await self.writer.drain()

    async def _recieve(self) -> bytes:
        """
        Read bytes from the socket based on the next header.

        No validation on the data is performed because this method simply uses the header to determine
        message length and returns that number of bytes. For most uses you should probably use :meth:`expect` instead.

        Returns:
            bytes: Raw bytes read from the socket not including the message header.
        """
        header = await self.reader.read(HEADER_LENGTH_BYTES)
        data_length = int.from_bytes(header)
        data = await self.reader.read(data_length)
        return data

    async def expect(
        self, length: int = -1, verifier: Optional[Callable[[bytes], Any]] = None
    ) -> Any:
        """
        Receive a message and optionally verify its content or length.

        This method reads a raw byte message from the stream, optionally checks its
        length, and applies a function to modify and further validate the content.

        Args:
            length: Expected length of the message. If greater than 0, the message length will
                be verified and raise a ValueError if the length does not match.
            verifier: A function that accepts an array of raw bytes and returns a processed or validated result.
                If None, returns the raw bytes.

        Returns:
            Any: The raw bytes, or the result of the verifier function.

        Raises:
            ValueError: If the message length does not match the expected length.
        """
        raw_bytes = await self._recieve()

        if length > 0 and len(raw_bytes) != length:
            raise ValueError(
                f"received data is not expected length (expected {length} but received {len(raw_bytes)})"
            )

        if verifier:
            return verifier(raw_bytes)
        else:
            return raw_bytes

    async def expect_str(self, length: int = -1) -> str:
        """
        Receive a UTF-8 string from the client with optional length validation.

        This method internally calls `expect` with a byte-to-string verifier, and
        checks the resulting string's length if specified.

        Args:
            length: Expected length of the decoded string. If greater than 0, a ValueError
                is raised if the decoded string does not match the given length.

        Returns:
            str: The decoded UTF-8 string.

        Raises:
            ValueError: If the decoded string's length does not match the expected length.
        """
        string = await self.expect(verifier=lambda bytes: bytes.decode())

        if length > 0 and len(string) != length:
            raise ValueError("received string is not expected length")

        return string

    async def error(self, message: str):
        """
        Send an error message to the client.

        The message string is encoded to UTF-8 and sent using the `send` method
        with the error flag set.

        Args:
            message: A human-readable error message to send to the client.
        """
        raw_bytes = message.encode()
        await self.send(raw_bytes, True)
