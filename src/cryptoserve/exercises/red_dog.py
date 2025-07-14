import math
import random
import time
from collections.abc import Generator

from cryptoserve.messaging import Client
from cryptoserve.types.errors import InvalidParameterError

MAX_ROUNDS = 10
STARTING_MONEY = 100
TARGET_MONEY = 1_000

CARDS_PER_SUIT = 13
CARDS_PER_DECK = 52
MODULUS = 256

from enum import IntFlag


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

    while 0 < money_remaining < TARGET_MONEY and rounds_completed < MAX_ROUNDS:
        await client.send(money_remaining.to_bytes(2))
        bet = await client.expect(verifier=verify_bet, money_remaining=money_remaining)

        dealt_cards = deal()

        message = dealt_cards[0].to_bytes(4) + dealt_cards[1].to_bytes(4)
        await client.send(message)

        guess = await client.expect(verifier=verify_guess)

        low_value, high_value, final_value = map(calculate_card_value, dealt_cards)
        correct_guess = "inside" if low_value < final_value < high_value else "outside"

        if guess == correct_guess:
            money_remaining += bet
            await client.send(
                dealt_cards[2].to_bytes(4), message_flags=RedDogExerciseFlags.WIN
            )
        else:
            money_remaining -= bet
            await client.send(
                dealt_cards[2].to_bytes(4), exercise_flags=RedDogExerciseFlags.LOSE
            )

        rounds_completed += 1

    await client.send(money_remaining.to_bytes(4))


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
    bet = int.from_bytes(received_data)

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

    return bet


def deal():
    while True:
        generator = random.choice(GENERATORS)
        generator.seed()

        cards_dealt = [generator.next(), generator.next()]
        cards_dealt.sort(key=calculate_card_value)
        low_value, high_value = map(calculate_card_value, cards_dealt[:2])

        if high_value - low_value >= 2:
            final_card = generator.next()
            cards_dealt.append(final_card)
            return cards_dealt
