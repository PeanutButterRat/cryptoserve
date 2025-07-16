import argparse
import socket
from enum import IntFlag

HEADER_LENGTH = 4


class MessageFlags(IntFlag):
    ERROR = 1 << 7


class ServerError(Exception):
    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data: bytes | str, server_flags: int = 0, exercise_flags: int = 0):
        if isinstance(data, str):
            data = data.encode()

        message_length = len(data).to_bytes(2)
        header = bytes([server_flags, exercise_flags, *message_length])
        message = header + data

        self.socket.sendall(message)

    def receive(self, include_flags: bool = False) -> bytes:
        header = self.socket.recv(HEADER_LENGTH)
        assert len(header) == HEADER_LENGTH, "received an invalid header"

        server_flags, exercise_flags = header[:2]
        message_length = int.from_bytes(header[2:])
        message = self.socket.recv(message_length)
        assert len(message) == message_length, "received an invalid message"

        if server_flags & MessageFlags.ERROR:
            message = message.decode()
            raise ServerError(message)

        return message if not include_flags else (server_flags, exercise_flags, message)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.socket.close()


def simple_hash(server: Server) -> None:
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(
        description="Client for connecting to a Cryptoserve server."
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="server host address"
    )
    parser.add_argument("--port", type=int, default=5050, help="server port")

    args = parser.parse_args()

    with Server(args.host, args.port) as server:
        greeting = server.receive()
        greeting = greeting.decode()
        print(greeting)

        try:
            selection = "Simple Hash"
            server.send(selection)

            start_message = server.receive()
            start_message = start_message.decode()
            print(start_message)

            simple_hash(server)

        except ServerError as error:
            print(error.message)


if __name__ == "__main__":
    main()
