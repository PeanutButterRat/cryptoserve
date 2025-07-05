.. _implementing_aes:

Implementing AES
================

In this exercise, users are tasked with implementing the major functions found within the AES specification
to get a deeper understanding of the algorithm.


Specification
-------------

Users are required to implement the following functions operations:

1. SBox
2. ShiftRows
3. MixColumns
4. SubBytes
5. KeyAddition

The protocol works like this:

1. The **server** generates a random number between 2 and 5, call this **x**. 
2. The **server** then sends randomly generated data over to the client which should perform SBox on the data and send it back.
3. The **server** checks for correctness and sends more data back to the client. This is exchange is performed a total of **x times**.
4. Steps **1 - 3** are repeated for the remaining operations in order: ShiftRows, MixColumns, SubBytes, KeyAddition.

The client can be determine what operation must be performed by examining bits **2 - 0** of the exercise flags.

::

     7   6   5   4   3   2   1   0
   +---+---+---+---+---+---+---+---+
   | 0 | 0 | 0 | 0 | 0 | x | x | x |
   +---+---+---+---+---+---+---+---+


Flag Meanings
-------------

+-------+--------------------------------------------------+
| Value | Meaning                                          |
+=======+==================================================+
| 0     | Perform KeyAddition* on the incoming bytes (32). |
+-------+--------------------------------------------------+
| 1     | Perform Sbox on the incoming byte (1).           |
+-------+--------------------------------------------------+
| 2     | Perform SubBytes on the incoming bytes (16).     |
+-------+--------------------------------------------------+
| 3     | Perform ShiftRows on the incoming bytes (16).    |
+-------+--------------------------------------------------+
| 4     | Perform MixColumns on the incoming bytes (16).   |
+-------+--------------------------------------------------+

\*When performing KeyAddition, the server will send 32 bytes of data. The first key is found in the first 16 bytes while the second key
is found in the second 16 bytes. Perform key addition with these two keys.


Extra Resources
---------------

- `AES Specification <https://csrc.nist.gov/pubs/fips/197/final>`_