.. _diffie_hellman_key_exchange:

Diffie-Hellman Key Exchange
===========================

In this exercise, users are tasked with implementing a simplified version of a DHKE.


Specification
-------------

1. The **server** starts off by by choosing a generator and and exponent. The server sends the chosen generator and key contribution together (one byte each).
2. The **client** uses the generator to complete the key. The client sends their key contribution back to the server.
3. The **server** responds with a block of data that has been encrypted with **AES-128 CBC mode** using the shared key along with the IV.
4. The **client** responds back with the decrypted plaintext to complete the exercise.


Group Details
^^^^^^^^^^^^^

With this exchange, the group to use is Z₂₅₁*. Because 251 is prime, Z₂₅₁* includes all the integers between 1 and 250 (inclusive).


Encryption Details
^^^^^^^^^^^^^^^^^^

In order to use AES with the Diffie-Hellman key, repeat the byte a total of 16 times to achieve the required
128-bit key size. Cipher block chaining also requires an initialization vector (IV) which is sent by the server.
In Step 3, the server sends 16 bytes of ciphertext to decrypt, and 16 bytes for the IV to use for decryption.


Flag Meanings
-------------

No flags are used in this exercise.


Sequence Diagram
----------------

.. uml::

  participant Client
  participant Server

  note over Server
    Server selects:
    - g ∈ Z₂₅₁*
    - a ∈ [1, φ(251) - 1]
  end note

  Server ->> Client : generator || gᵃ mod 251

  note over Client
    Client selects:
    - b ∈ [1, φ(251) - 1]
  end note

  Client -->> Server : gᵇ mod 251

  note over Client, Server
    k = (gᵃ)ᵇ and (gᵇ)ᵃ
  end note

  note over Server
    - key = [k, k, k, ..., k] (16 bytes)
    - data = [16 random bytes]
    - iv = [16 random bytes]
    - ciphertext = AES_CBC_encrypt(data, key, iv)
  end note

  Server ->> Client : ciphertext || iv

  note over Client
    - plaintext = AES_CBC_decrypt(data, key, iv)
  end note

  Client -->> Server : plaintext

.. note:: ``||`` as shown above means to concatenate byte strings together as a single chunk of data.
