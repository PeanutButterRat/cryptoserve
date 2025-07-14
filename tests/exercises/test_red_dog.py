import pytest

from cryptoserve.exercises.red_dog import red_dog
from cryptoserve.messaging import Client
from cryptoserve.types.errors import InvalidParameterError
from tests.utils import simulate_exercise

ONE_HUNDRED = b"\x00\x64"
TWO_HUNDRED = b"\x00\xc8"
FOUR_HUNDRED = b"\x01\x90"
EIGHT_HUNDRED = b"\x03\x02"


class MockGenerator:
    def __init__(self, values: list[int]):
        self.values = values
        self.index = 0

    def next(self):
        value = self.values[self.index]
        self.index = (self.index + 1) % len(self.values)
        return value

    def seed(self):
        pass


@simulate_exercise(received_data=[EIGHT_HUNDRED + b"I"])
async def test_invalid_bet(client: Client):
    with pytest.raises(InvalidParameterError):
        await red_dog(client)


@simulate_exercise(received_data=[ONE_HUNDRED + b"X"])
async def test_invalid_guess(client: Client):
    with pytest.raises(InvalidParameterError):
        await red_dog(client)


@simulate_exercise(
    received_data=[
        ONE_HUNDRED + b"I",
        TWO_HUNDRED + b"O",
        FOUR_HUNDRED + b"I",
        EIGHT_HUNDRED + b"O",
    ],
    patches={
        "cryptoserve.exercises.red_dog.GENERATORS": [MockGenerator([0, 11, 2, 2, 6, 7])]
    },
)
async def test_successful_completion(client: Client):
    await red_dog(client)
