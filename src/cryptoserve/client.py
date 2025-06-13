import socket

import numpy as np

HOST = "127.0.0.1"
PORT = 5050

np.seterr(over="ignore")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        print(receive(sock).decode())

        selection = input("\nSelection: ")
        send(selection.encode(), sock)

        hash = simple_hash("Hello, World!", sock)

        print(hex(hash))


def simple_hash(message: str, sock: socket.socket):
    data = message.encode()
    data_length = len(data)
    padding = 4 - data_length % 4
    padded_data = data.ljust(data_length + padding, b"\0")
    send(len(padded_data).to_bytes(2), sock)
    hash = np.uint16(data_length)

    for i, chunk in enumerate(zip(padded_data[::2], padded_data[1::2])):
        chunk = np.uint16(int.from_bytes(chunk))

        if i % 2 == 0:
            hash = f(hash, chunk)
        else:
            message = int(hash).to_bytes(2) + int(chunk).to_bytes(2)
            send(message, sock)

            message = receive(sock)
            hash = np.uint16(int.from_bytes(message))

    return hash


def receive(sock: socket.socket):
    data_length = int.from_bytes(sock.recv(2))
    return sock.recv(data_length)


def send(data: bytes, sock: socket.socket):
    raw_bytes = len(data).to_bytes(2) + data
    sock.sendall(raw_bytes)


def f(a: np.uint16, b: np.uint16):
    a ^= b + 0xC0DE
    return (a << 3) | (a >> 13)


if __name__ == "__main__":
    main()
