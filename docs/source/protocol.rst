.. _protocol:

Messaging Protocol
==================

Cryptoserve uses low-level **TCP sockets** to communicate with its clients.  Since TCP is stream-oriented, a socket only
sees a sequence of bytes being sent back and forth. Because of this, a protocol must be designed in order to facillitate
a logical conversation between client and server.


Message Structure
-----------------

The overall structure of a message (packet) in Cryptoserve constitutes of two parts:

1. Header
2. Data

The overall purpose of the message header is to notify a recipient of how much data should be expected in the next message
as well as give some insight on how that data should be interpreted.


Header Format
-------------

The message header is **two-bytes** in size and can be interpreted as an unsigned **16-bit unsigned integer** in 
**big-endian** order. The **most significant nibble** (4 bits), is reserved for message flags. 
Currently, only the first bit has meaning while the other three are reserved for future use or for exercise-specific purposes.

=================  =====  ===============================================
Bit(s)             Name   Description
=================  =====  ===============================================
15 (MSB)           ERR    *Error flag*.
14 - 12                   *Unused*. Reserved for future flags or exercises.
14 … 0             LEN    *Payload length* in bytes.
=================  =====  ===============================================

.. note::  Because there are 12 bits used for the message length field, the maximum payload size is 4095 bytes (``0x0FFF``).


Flags
-----

Error
^^^^^

The **error flag** is used to indicate that the client has done something wrong in the exchange and 
subsequently failed the exercise. The following data is encoded as a UTF-8 string that contains hints
about what went wrong for debugging purposes on the client side. The socket is also closed after an
error message is sent.

.. note:: Errors only have meaning if they are sent from the server to the client. The server ignores this bit field entirely.


Diagram
-------

The following diagram is a visual representation of how the bits are arranged in a complete message.

::

    Bits:     15    14    13    12    11...                       ...0
              +-----+-----+-----------+------------------------------+--------------------------------+
    Purpose:  | ERR |     |     |     | Data Length                  | Data  (<= 32,767 bytes)        |
              +-----------+-----------+------------------------------+--------------------------------+


Examples
--------

Here are some examples of how certain data would be sent over the network. Be mindful that
the data representation swaps between binary and hex.

1. Sending a string: ***Hello, World!**

::

   Header        : 0000 0000 0000 1101 -> 00 0D
   Data          : "Hello, World!"     -> 48 65 6C 6C 6F 2C 20 57 6F 72 6C 64 21
   Complete frame: 00 0D 48 65 6C 6C 6F 2C 20 57 6F 72 6C 64 21
   
   15    14    13    12    11...              ...0
   +-----+-----+-----------+---------------------+----------------------------+
   |  0  |  x  |  x  |  x  | 0000 0000 0000 1101 | 1001000 1100101 1101100... |
   +-----------+-----------+---------------------+----------------------------+


2. Sending an integer: **0xDEADBEEF**.

::

   Header        : 0000 0000 0000 0100 -> 0004
   Payload       : DE AD BE EF          -> DE AD BE EF
   Complete frame: 00 04 DE AD BE EF
   
   15    14    13    12    11...              ...0
   +-----+-----+-----------+---------------------+----------------------------+
   |  0  |  x  |  x  |  x  | 0000 0000 0000 1101 | 1001000 1100101 1101100... |
   +-----------+-----------+---------------------+----------------------------+


3. Sending an **error**.

::

   Header        : 1000 0000 0001 1011  -> 80 1B
   Payload       : "Incorrect padding!" -> 49 6e 63 6f 72 72 65 63 74 20 70 61 64 64 69 6e 67 21
   Complete frame: 80 1B 49 6E 70 75 74 20 77 61 73 20 70 61 64 64 65 64 20 69 6E 63 6F 72 72 65 63 74 6C 79
   
   15    14    13    12    11...              ...0
   +-----+-----+-----------+---------------------+----------------------------+
   |  1  |  x  |  x  |  x  | 0000 0000 0000 1101 | 1001001 1101110 1100011... |
   +-----------+-----------+---------------------+----------------------------+
