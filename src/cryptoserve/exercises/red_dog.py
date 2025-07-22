import random
import time
from enum import IntFlag

from cryptoserve.messaging import Client
from cryptoserve.types import ExerciseError, InvalidParameterError

MAX_ROUNDS = 10
STARTING_MONEY = 100
TARGET_MONEY = 1_000

CARDS_PER_SUIT = 13
CARDS_PER_DECK = 52
MODULUS = 256
INSIDE_GUESS = "I"
OUTSIDE_GUESS = "O"


class RedDogExerciseFlags(IntFlag):
    WIN = 1
    LOSE = 2


class LCG:
    def __init__(self, modulus: int, a: int, c: int, seed: int = 0):
        self.modulus = modulus
        self.a = a
        self.c = c
        self.value = seed

    def next(self):
        self.value = (self.a * self.value + self.c) % self.modulus
        return self.value

    def get_period(self):
        seen = set()
        value = self.value

        while value not in seen:
            seen.add(value)
            value = self.next()

        return len(seen)

    def seed(self, seed: int = int(time.time())):
        self.value = seed % self.modulus


GENERATORS = []

for a in range(MODULUS):
    for c in range(MODULUS):
        generator = LCG(MODULUS, a, c)
        if generator.get_period() == MODULUS:
            GENERATORS.append(generator)


async def red_dog(client: Client) -> None:
    money_remaining = STARTING_MONEY
    rounds_completed = 0

    generator = random.choice(GENERATORS)
    generator.seed()

    while 0 < money_remaining < TARGET_MONEY and rounds_completed < MAX_ROUNDS:
        await client.send(money_remaining.to_bytes(2))

        dealt_cards = [generator.next() for card in range(3)]
        message = dealt_cards[0].to_bytes() + dealt_cards[1].to_bytes()
        await client.send(message)

        bet, guess = await client.expect(
            verifier=verify_bet, length=3, money_remaining=money_remaining
        )

        card_values = list(map(calculate_card_value, dealt_cards))
        low_value, high_value = sorted(card_values[:2])
        final_value = card_values[-1]

        correct_guess = (
            INSIDE_GUESS if low_value < final_value < high_value else OUTSIDE_GUESS
        )

        if guess == correct_guess:
            money_remaining += bet
            await client.send(
                dealt_cards[2].to_bytes(), exercise_flags=RedDogExerciseFlags.WIN
            )
        else:
            money_remaining -= bet
            await client.send(
                dealt_cards[2].to_bytes(), exercise_flags=RedDogExerciseFlags.LOSE
            )

        rounds_completed += 1

    if money_remaining < TARGET_MONEY:
        raise ExerciseError(
            error="failed to hit the target goal",
            explanation=f"You failed to hit ${TARGET_MONEY} in under {MAX_ROUNDS} rounds. You only acheived ${money_remaining}.",
            hints=[
                "Are you betting enough money each round to be able to hit the target?",
                "Are you leveraging your knowledge of LCG's to accurately predict the next value?",
            ],
        )


def calculate_card_value(card: int) -> int:
    card = (card % CARDS_PER_DECK) + 1
    card = (card % CARDS_PER_SUIT) + 1
    return card


def verify_guess(received_data: bytes) -> str:
    guess = received_data.decode().lower()

    if guess not in ["inside", "outside"]:
        raise InvalidParameterError()

    return guess


def verify_bet(received_data: bytes, money_remaining: int) -> int:
    bet = int.from_bytes(received_data[:2])
    guess = received_data[2:].decode().upper()

    if guess not in [INSIDE_GUESS, OUTSIDE_GUESS]:
        raise InvalidParameterError(
            error=f"guess must be {INSIDE_GUESS} or {OUTSIDE_GUESS}"
        )

    if bet < 0:
        raise InvalidParameterError(
            error="bet cannot be negative",
            explanation="You placed an invalid bet. Your bet must be non-negative.",
        )

    if bet > money_remaining:
        raise InvalidParameterError(
            error="bet is too high",
            explanation=f"You don't have enough money to cover your bet. You tried to place a ${bet} bet with only ${money_remaining} remaining.",
        )

    return bet, guess
