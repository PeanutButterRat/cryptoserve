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
    "--host", type=str, default="127.0.0.1", help="host address to bind to"
)

argparser.add_argument(
    "--port", "-p", type=int, default=5050, help="port number to bind to"
)


def main():
    args = argparser.parse_args()

    if not (0 <= args.port <= 65535):
        argparser.error("port must be in range 0-65535")

    asyncio.run(serve(args.host, args.port))
