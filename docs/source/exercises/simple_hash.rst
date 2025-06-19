.. _custom_hash_protocol:

Simple Hash
====================

The following describes a toy hash algorithm intuitively named **Simple Hash**.
This algorithm processes input data in pairs of bytes and alternates between two 
compression functions to iteratively compute a **16-bit hash**.


Specification
-------------

**Simple Hash** works as follows:

1. **Determine the data** to hash. This must be a sequence of bytes **no greater than 255 bytes long**.
2. Set the initial hash to a sequence of two bytes, both set to the **length of the data**. Treat this as a 16-bit unsigned integer.
3. **Pad the initial data** with null bytes so its length is a **multiple of 4**.
4. **Split** the padded data into **2-byte chunks**.
5. **Apply two compression functions** to the hash and the next chunk of data until the data is exhausted, alternating each iteration.
6. The final result of the last iteration is the resulting hash.


Padding
^^^^^^^

The hash input is padded with null bytes (**x00**) to make its length a multiple of 4.
This is accomplished by adding to the end of the data until its length is the **next largest mulitple of four**.

.. note::

   This padding scheme ensures the input can be cleanly divided into 2-byte chunks for even alternation the compression functions.


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

1. The **client** first **picks the input data** and sends it to the server.
2. The **server** responds with an **OK** message.
3. The **client pads** the data's length to a mulitple of 4 and sends the padded data to the **server**.
4. The **server** responds with an **OK** message.
5. The **client applies f** to the hash and 2 bytes of input data.
6. The **client** sends the hash to the **server**.
7. The **server applies g** to the recieved hash and next chunk of data.
8. The **server** sends the new hash back to the client.
9. Steps **5 - 8 are repeated** until the input is exhausted.


Sequence Diagram
^^^^^^^^^^^^^^^^

Here is a visual representation of the client-server interaction where...

- **hᵢ** is the i-th hash value.
- **h₀** is the initial hash before consuming any input data.
- **cᵢ** is the i-th chunk of input data.
- **n** is the total number of chunks to be hashed.

.. mermaid::

   sequenceDiagram
      participant Client
      participant Server

      Client->>Server: Input
      Server-->>Client: OK

      Client->>Server: Padded Input
      Server-->>Client: OK

      Note over Client: h₀ ← [Input.length, Input.length]
      Note over Client: h₁ ← f(h₀, c₁)
      Client->>Server: h₁

      Note over Server: h₂ ← g(h₁, c₂)
      Server-->>Client: h₂

      loop for (i = 3, i < n, i += 2)
         Note over Client: hᵢ ← f(hᵢ₋₁, cᵢ)
         Client->>Server: hᵢ

         Note over Server: hᵢ₊₁ ← g(hᵢ, cᵢ₊₁)
         Server-->>Client: hᵢ₊₁
      end

      Note over Client, Server: Final Hash = hₙ


Example
-------

The following example demonstrates how the string **Apple** is hashed using this algorithm.


Initial Hash
^^^^^^^^^^^^

The initial hash **h₀** is set to the length of the data, stored in both the high and low bytes of the hash.

.. code-block:: text

   Input.length = 0x05
   h₀ = 0x 05 05


Padding
^^^^^^^

Now the input must be padded because the length of **Apple** is not an even multiple of 4.
The next largest multiple is 8, so the 3 null bytes must be added to the end of the **Apple**.
To do this, we encode the string using **UTF-8** and then add null bytes.

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

      Client->>Server: 0x4170706C65
      Server-->>Client: OK

      Client->>Server: 0x 4170706C65000000
      Server-->>Client: OK

      Note over Client: h₀ ← 0x0505

      loop chunk 1
         Note over Client: h₁ ← f(0x0505, 0x4170) = 0x0703
         Client->>Server: h₁
      end

      loop chunk 2
         Note over Server: h₂ ← g(0x0703, 0x706C) = 0x140D
         Client->>Server: h₂
      end

      loop chunk 3
         Note over Client: h₃ ← f(0x140D, 0x6500) = 0x8E99
         Client->>Server: h₃
      end

      loop chunk 4
         Note over Server: h₄ ← g(0x8E99, 0x0000) = 0x181A
         Client->>Server: h₄
      end

      Note over Client, Server: Final Hash = h₄ = 0x181A

Therefore, the **Simple Hash** of **Apple** is 0x181A.
