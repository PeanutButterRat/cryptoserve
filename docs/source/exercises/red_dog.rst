.. _red_dog:

Red Dog
=======

In this exercise, users are tasked with exploring the weaknesses of pseudo-random number generators,
specifically by a `linear congruential generator (LCG) <https://en.wikipedia.org/wiki/Linear_congruential_generator>`_.


What is Red Dog?
----------------

`Red Dog <https://en.wikipedia.org/wiki/Red_dog_(card_game)>`_ is a card game that is featured in mostly online casinos.
It works as follows:

1. The player places a monetary wager.
2. Two cards are dealt face up.
3. The player now bets whether or not the next card's value will fall between the two cards (inside the spread) or not (outside the spread).
4. The player is awarded with money based on the outcome and how large the spread is (difference in value between the low card and high card).

The Cryptoserve Casino™
-----------------------

The **Cryptoserve Casino™** offers the ability to play Red Dog over the internet. As a player, your job is to maximize the amount of
money you can earn by leveraging your knowledge about psuedo-randomness. You suspect the online casino is using a LCG to generate 
card values by generating a **random byte** and then **mapping that value to card number**.

Can you use this information to cheat the system and walk away with a lot of money?

Specification
-------------

When playing Red Dog, you will start off with $100 in initial funds. You goal is to 10x your money by acheiving $1,000 in under 10 rounds or less.
You must do this by exploiting the properties of a LCG to predict the next value.

The protocol works by the following:

1. The **server** starts a round by sending the remaining cash as a two-byte unsigned integer.
2. The **server** deals two cards and sends them to the client. These are represented as single bytes.
3. The **client** responds with their bet for the next round. The first two bytes of this response is their monetary bet while the third bet is either **"I"** for inside the spread or **"O"** for outside the spread.
4. The **server** deals the last card and sends it back to the client with the appropriate flag set depending on the outcome.
5. Steps **1 - 4** are repeated until the client hits the goal, runs out of money, or runs out of rounds. 

.. note::

   For the sake of simplicity, the traditional game of **Red Dog** has been altered slightly to make it easier to work with. In a real game, the money
   you win depends on the size of the spread, but here you will either win double your initial bet or lose it (i.e. "double or nothing").
   
   In real **Red Dog**, pushes occur when the spread is too small. For example, imagine the dealer deals a **7 of Hearts** and an **8 of Clubs**. Because there are no cards that fit in the
   spread, the player receives their initial bet and the round ends like nothing happened (i.e. a "push"). In this version, **pushes are ignored** so you must set your bet accordingly if there is no chance
   of winning a given round.


Flag Meanings
-------------

Exercise Flags are used in this exercise to notify the client whether they **won or lost the previous round** when the final
card is dealt.

::

     7   6   5   4   3   2   1   0
   +---+---+---+---+---+---+---+---+
   | 0 | 0 | 0 | 0 | 0 | 0 | x | x |
   +---+---+---+---+---+---+---+---+

+-------+--------------------------------------------------+
| Bit   | Meaning                                          |
+=======+==================================================+
| 0     | You placed a winning bet on the last round.      |
+-------+--------------------------------------------------+
| 1     | You placed a losing bet on the last round.       |
+-------+--------------------------------------------------+

Card Mapping
-------------

To generate card values, the server generates a **random byte** and **mods it by 52** to generate a value that maps to
one of the possible cards in a **standard 52-card deck**. Because suit doesn't matter for this game, the actual card value
used to determine the spread is calculated by further **modding the value by 4** (the number of suits) and then **adding one**
to acheive a final value between **1 and 13 (inclusive)**.

.. math::

   Value = ((byte \bmod Cards/Deck) \bmod Suits/Deck) + 1


Extra Resources
---------------

- `LCG (Wikipedia) <https://en.wikipedia.org/wiki/Linear_congruential_generator>`_.