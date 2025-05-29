import socket

HOST = "127.0.0.1"
PORT = 5050


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(b"Ping\n")
        data = sock.recv(1024)

    print(f"Received: {data.decode()}")


if __name__ == "__main__":
    main()
