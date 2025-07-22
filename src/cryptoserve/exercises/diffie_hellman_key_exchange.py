import math
import os
import random

from Crypto.Cipher import AES

from cryptoserve.messaging import Client
from cryptoserve.types import DataMismatchError

MODULUS = 251


def find_multiplicative_group(modulus: int) -> list[int]:
    group = []

    for i in range(modulus):
        if math.gcd(i, modulus) == 1:
            group.append(i)

    return group


def find_generators(group: list[int], modulus: int) -> bool:
    generators = []

    for member in group:
        generated = set()
        current = member % modulus

        while current not in generated:
            generated.add(current)
            current = (current * member) % modulus

        if len(generated) == len(group):
            generators.append(member)

    return generators


z_star_251 = find_multiplicative_group(MODULUS)
z_star_251_generators = find_generators(z_star_251, MODULUS)

print(len(z_star_251))

async def diffie_hellman_key_exchange(client: Client) -> None:
    generator = random.choice(z_star_251_generators)
    exponent = random.randint(1, len(z_star_251) - 1)
    server_key_contribution = pow(generator, exponent, MODULUS)

    message = generator.to_bytes() + server_key_contribution.to_bytes()
    await client.send(message)

    client_key_contribution = (await client.expect(length=1))[0]
    key = pow(client_key_contribution, exponent, MODULUS)

    key = bytes([key] * 16)
    data = os.urandom(16)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(data)

    message = ciphertext + cipher.iv
    await client.send(message)

    plaintext = await client.expect(16)

    if data != plaintext:
        raise DataMismatchError(
            error="plaintext does not match the original data",
            explanation=f"The plaintext the server received did not match the original data generated. The server encrypted '{data}' but received {plaintext}.",
            hints=[
                "Are you parsing the data from the server as the IV and plaintext correctly?",
                "Are you using the correct mode of decryption for AES?",
            ],
        )
