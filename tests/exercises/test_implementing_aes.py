import aes
import pytest
from Crypto.Cipher import AES
from Crypto.Util import Counter, Padding

from cryptoserve.exercises.implementing_aes import implementing_aes
from cryptoserve.messaging import Client
from cryptoserve.types import DataMismatchError
from tests.utils import simulate_exercise


@pytest.mark.parametrize(
    "key, iv, pt",
    [
        (
            0x000102030405060708090A0B0C0D0E0F,
            0x00000000000000000000000000000000,
            0x00112233445566778899AABBCCDDEEFF,
        ),
        (
            0x2B7E151628AED2A6ABF7158809CF4F3C,
            0xF0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF,
            0x6BC1BEE22E409F96E93D7E117393172A,
        ),
        (
            0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,
            0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB,
            0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC,
        ),
        (
            0x01010101010101010101010101010101,
            0x02020202020202020202020202020202,
            0x03030303030303030303030303030303,
        ),
        (
            0x00112233445566778899AABBCCDDEEFF,
            0xDEADBEEFDEADBEEFDEADBEEFDEADBEEF,
            0x11223344556677889900AABBCCDDEEFF,
        ),
    ],
)
def test_ctr_mode_aes128_against_pycryptodome(key: int, iv: int, pt: int):
    cipher = aes.aes(key, 128, mode="CTR", iv=iv)
    ctr = Counter.new(128, initial_value=iv)
    key, iv, pt = map(lambda x: x.to_bytes(16), [key, iv, pt])
    reference = AES.new(key, AES.MODE_CTR, counter=ctr)

    actual = bytes(cipher.enc(list(pt)))
    expected = reference.encrypt(Padding.pad(pt, 16))
    assert actual == expected, "encryption does not behave properly"

    reference = AES.new(key, AES.MODE_CTR, counter=ctr)
    actual = bytes(cipher.dec(actual))
    expected = Padding.unpad(reference.decrypt(expected), 16)
    assert actual == expected, "decryption does not behave properly"


deterministic_patches = {
    "os.urandom": lambda n: b"\x00" * n,
    "random.randint": lambda *_: 1,
}


@simulate_exercise(
    sent_data=["\x00" * 32, "\x00"],
    received_data=["\x00" * 16, "\x64"],
    patches=deterministic_patches,
)
async def test_sbox_implementation(client: Client):
    with pytest.raises(DataMismatchError):
        await implementing_aes(client)


@simulate_exercise(
    sent_data=[
        ("\x00" * 32, None, 0),
        ("\x00", None, 1),
        ("\x00" * 16, None, 2),
        ("\x00" * 16, None, 3),
        ("\x00" * 16, None, 4),
    ],
    received_data=["\x00" * 16, "\x63", "\x63" * 16, "\x00" * 16, "\x00" * 16],
    patches=deterministic_patches,
)
async def test_successful_completion(client: Client):
    await implementing_aes(client)
