"""The command-line entry point for Cryptoserve."""

import argparse
import asyncio

from cryptoserve.server import serve


class ArgparseFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.MetavarTypeHelpFormatter
):
    pass


argparser = argparse.ArgumentParser(
    prog="Cryptoserve",
    description="Server software that houses a library of cryptography-related learning exercises.",
    formatter_class=ArgparseFormatter,
)

argparser.add_argument(
    "--host", type=str, default="0.0.0.0", help="host address to bind to"
)

argparser.add_argument(
    "--port", "-p", type=int, default=5050, help="port number to bind to"
)

argparser.add_argument(
    "--timeout",
    "-t",
    type=int,
    default=60,
    help="time in seconds the server waits for a response before closing an unresponsive connection",
)


def main():
    """The main entry point for Cryptoserve.

    Creates and runs the main server.
    """
    args = argparser.parse_args()

    if not (0 <= args.port <= 65535):
        argparser.error("port must be in range 0-65535")

    asyncio.run(serve(args.host, args.port, args.timeout))


if __name__ == "__main__":
    main()
