"""Interface for facilitating communication between the client and server.

This module defines the ``Client`` class which abstracts the details away of the network protocol. It handles the details
of encapsulating data for transmission so the developer can concern themselves with the data themselves instead of
worrying about the protocol details. It also provides some utilities for error-checking data received from a client
during the course of an exercise.
"""

import asyncio
import inspect
from enum import IntFlag
from typing import Any, Callable, Optional

from cryptoserve.types import DataTransmissionError

HEADER_LENGTH_BYTES = 4
OK_MESSAGE = "OK"


class MessageFlags(IntFlag):
    ERROR = 1 << 7


def add_header(data: bytes, server_flags: int = 0, exercise_flags: int = 0) -> bytes:
    header = bytearray(HEADER_LENGTH_BYTES)
    header[:2] = server_flags, exercise_flags
    header[2:] = len(data).to_bytes(2)

    return bytes(header + data)


def parse_header(header: bytes) -> tuple[int, int, int]:
    assert len(header) == HEADER_LENGTH_BYTES
    server_flags, exercise_flags = header[:2]
    data_length = int.from_bytes(header[2:])

    return data_length, server_flags, exercise_flags


class Client:
    """Interface for sending and receiving data from a user.

    This class is used as an interface for sending and receiving data from a socket between the client and server.
    It provides various utilities to abstract the underlying protocol information to send blobs of data back and
    forth in an asynchronous manner.
    """

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        timeout: int = 5,
    ):
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
        self.timeout = timeout

    async def _read(self, n: int) -> bytes:
        async with asyncio.timeout(self.timeout):
            data = await self.reader.readexactly(n)
            return data

    async def receive(self) -> bytes:
        async with asyncio.timeout(self.timeout):
            header = await self._read(HEADER_LENGTH_BYTES)
            data_length, server_flags, exercise_flags = parse_header(header)
            received_data = await self._read(data_length)
            return received_data, server_flags, exercise_flags

    async def _write(self, data: bytes):
        """Write to the socket.

        This method should be used to write data to the socket connection instead of interacting with the StreamWriter
        directly in order to make the class easier to mock during testing.

        Args:
            data: The raw bytes to send.
        """
        async with asyncio.timeout(self.timeout):
            self.writer.write(data)
            await self.writer.drain()

    async def send(
        self,
        data: bytes | str,
        server_flags: int | MessageFlags = 0,
        exercise_flags: int | MessageFlags = 0,
    ):
        """Send a collection of bytes to the client.

        Args:
            data: The bytes to send.
            server_flags: The server flags to use in the message header. Defaults to 0.
            exercise_flags: The exercise flags to use in the message header. Defaults to 0.
        """
        async with asyncio.timeout(self.timeout):
            if isinstance(data, str):
                data = data.encode()

            message = add_header(data, int(server_flags), int(exercise_flags))
            await self._write(message)

    async def expect(
        self,
        length: int = -1,
        verifier: Optional[Callable[[bytes], Any]] = None,
        **kwargs,
    ) -> Any:
        """Receive a message and optionally verify its content or length.

        This method reads a raw byte message from the stream, optionally checks its
        length, and applies a function to modify and further validate the content.

        Args:
            length: Expected length of the message. If greater than 0, the message length will
                be verified and raise a DataTransmissionError if the length does not match.
            verifier: A function that accepts an array of raw bytes and returns a processed or validated result.
                If None, returns the raw bytes. See :ref:`verifier-parameters` for more details.

        Returns:
            Any: The raw bytes, or the result of the verifier function.

        Raises:
            DataTransmissionError: If the message length does not match the expected length.
        """
        async with asyncio.timeout(self.timeout):
            received_data, server_flags, exercise_flags = await self.receive()

            if length > 0 and len(received_data) != length:
                raise DataTransmissionError(
                    f"expected {length} byte{'s' if length > 1 else ''} but received {len(received_data)} instead"
                )

            if verifier:
                signature = inspect.signature(verifier)
                arguments = {}

                for key, value in [
                    ("received_data", received_data),
                    ("server_flags", server_flags),
                    ("exercise_flags", exercise_flags),
                ]:
                    if key in signature.parameters:
                        arguments[key] = value

                return verifier(**arguments, **kwargs)

            else:
                return received_data

    async def expect_str(self, length: int = -1) -> str:
        """Receive a UTF-8 string from the client with optional length validation.

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
        async with asyncio.timeout(self.timeout):
            string = await self.expect(
                verifier=lambda received_data: received_data.decode()
            )

            if length > 0 and len(string) != length:
                raise DataTransmissionError(
                    f"expected string of length {length} but received string of length {len(string)})"
                )

            return string

    async def error(self, message: str):
        """Send an error message to the client.

        The message string is encoded to UTF-8 and sent using the `send` method
        with the error flag set.

        Args:
            message: A human-readable error message to send to the client.
        """
        async with asyncio.timeout(self.timeout):
            raw_bytes = message.encode()
            await self.send(raw_bytes, server_flags=MessageFlags.ERROR)

    async def ok(self):
        """Send an OK message to the client.

        Sends the string "OK" to the client. Use this to confirm data sent by the client
        when no other response is applicable.
        """
        async with asyncio.timeout(self.timeout):
            raw_bytes = OK_MESSAGE.encode()
            await self.send(raw_bytes)
