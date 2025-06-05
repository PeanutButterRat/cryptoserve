.. _custom_hash_protocol:

Simple Hash
====================

The following describes a toy hash algorithm intuitively named **Simple Hash**.
This algorithm processes input data in pairs of bytes and alternates between two 
compression functions to iteratively compute a 16-bit hash.


Specification
-------------

**Simple Hash** works as follows:

1. The initial hash value is set to the **length of the input**, interpreted as a 16-bit unsigned integer.
2. The input data is **padded** with null bytes so its length is a multiple of 4.
3. The padded data is split into **2-byte chunks**.
4. An **alternating compression function** is applied to the current hash and the next chunk of data in order until the input is exhausted. The function used in a given round **alternates every chunk**.
5. The final result of the last iteration is the resulting hash.

.. note::

   Because the length of the input is used to "seed" the hash which is stored as a 16-bit unsigned integer, the input can not be any longer than **65,535 bytes**.


Padding
^^^^^^^

The hash input is padded with null bytes (**x00**) to make its length a multiple of 4.
This is accomplished by adding to the end of the data until its length is the **next largest mulitple of four**.

.. note::

   This padding scheme ensures the input can be cleanly divided into 2-byte chunks for even alternation between the client and server.


Compression Functions
^^^^^^^^^^^^^^^^^^^^^

The two compression functions used are defined as follows:

.. code-block:: python

   def f(a: uint16, b: uint16):
      temp = a ^ (b + 0xC0DE)
      temp = temp ROTL 3  # Left bitwise rotation of temp.
      return temp

   def g(a: uint16, b: uint16):
      temp = a ^ (b + 0xBEAD)
      temp = temp >> 1  # Right bitshift of temp.
      return temp

Both functions accept two 16-bit unsigned integers and combine them to return a single 16-bit unsigned integer.
During hashing, **f** is applied first on **odd iterations** followed by **g** on **even iterations**.


Final Output
^^^^^^^^^^^^

The output of **Simple Hash** is a 2-byte digest representing the final hash state.


Client-Server Protocol
----------------------

**Simple Hash** is further extended to a client-server model in the following way:

1. The **client** first picks the input data and pads its length to a mulitple of 4.
2. The **client applies f** to the initial hash and first 2 bytes of data.
3. The client sends the **resulting hash** and the **next 2-byte chunk** to the server.
4. The **server applies g** and returns the new hash.
5. The client applies **f** again on the returned hash and next chunk
6. Steps **3 - 5 are repeated** until the input is exhausted.


Sequence Diagram
^^^^^^^^^^^^^^^^

Here is a visual representation of the client-server interaction where...

- **hᵢ** is the i-th hash value.
- **cᵢ** is the i-th chunk of input data.
- **n** is the total number of chunks to be hashed.

.. mermaid::

   sequenceDiagram
      participant Client
      participant Server

      Note over Client: h₀ ← f(input.length)
      Client->>Server: h₀, c₁
      Note over Server: h₁ ← g(h₀, c₁)
      Server-->>Client: h₁

      loop while i < n
         Note over Client: hᵢ ← f(hᵢ₋₁, cᵢ)
         Client->>Server: hᵢ, cᵢ₊₁
         Note over Server: hᵢ₊₁ ← g(hᵢ, cᵢ₊₁)
         Server-->>Client: hᵢ₊₁
      end

      Note over Client, Server: Final Hash = hₙ


Example
-------

The following example demonstrates how the string **Apple** is hashed using this algorithm.


Initial Hash
^^^^^^^^^^^^

The initial hash **h₀** is set to the length of the data.

.. code-block:: text

   h₀ = input.length = 0x0005


Padding
^^^^^^^

Now the input must be padded because the length of **Apple** is not an even multiple of 4.
The next largest multiple is 8, so the 3 null bytes must be added to the end of the **Apple**.

.. code-block:: text

   Apple → 0x 41 70 70 6C 65 → Padding → 0x 41 70 70 6C 65 00 00 00


Data Exchange
^^^^^^^^^^^^^

.. note::

   The use of **loop** here is solely intended to visually section off each chunk of data.

.. mermaid::

   sequenceDiagram
      participant Client
      participant Server

      loop chunk 1
         Note over Client: f(h₀, 0x4170) = 0x1258 → h₁
         Client->>Server: (h₁, 0x706C)
      end

      loop chunk 2
         Note over Server: g(h₁, 0x706C) = 0x1EA0 → h₂
         Server-->>Client: h₂
      end

      loop chunk 3
         Note over Client: f(h₂, 0x6500) = 0xDBF1 → h₃
         Client->>Server: (h₃, 0x0000)
      end

      loop chunk 4
         Note over Server: g(h₃, 0x0000) = 0x32AE → h₄
         Server-->>Client: h₄
      end

      Note over Client, Server: Final Hash = h₄ = 0x32AE

Therefore, the hash of **Apple** is 0x32AE.
