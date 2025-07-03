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

The message header is **four bytes** in size. The two most significant bytes (first two) are reserved for message flags
while the least significant (last two) are reserved for the message size. The most significant flag byte is reserved for
server flags which give the user notice about how to interpret the message while the other flag byte is reserved for
exercise use if needed. Here is a visual diagram that shows the number of bits in each field. Please note that the numbers
shown are **not** the bit numbers used in the rest of the documentation as they are reversed (i.e. bit 0 in the diagram is
actually bit 7 of the server flags).

.. mermaid::

  ---
  title: "Header Format (bits)"
  ---
  packet-beta
    0-7: "Server Flags"
    8-15: "Exercise Flags"
    16-31: "Message Length"

.. note::  Because there are 16 bits used for the message length field, the maximum payload size is **65535** bytes (2¹⁶ - 1).


Server Flags
------------

Server flags are used to convey to the user information about what has happened during the exchange or how to
interpret some type of data. Most flags are not currently used but may be added in future versions of the software.

=========  =====  ===================================
Bit(s)     Name   Description
=========  =====  ===================================
7 (MSB)    ERROR  *Error flag*. An error occurred.
6 … 0             *Unused*. Reserved for future use.
=========  =====  ===================================

Error
^^^^^

**Bit 7 (MSB)**. The **error flag** is used to indicate that the client has done something wrong in the exchange and 
subsequently failed the exercise. The data sent alongside the message is encoded as JSON data in UTF-8
that contains hints about what went wrong for debugging purposes on the client side. The socket is also closed after an
error message is sent.

.. note:: Errors currently only have meaning if they are sent from the server to the client. The server ignores this bit field entirely.


Examples
--------

Here are some examples of how certain data would be sent over the network. Be mindful that
the data representation swaps between binary and hex.

1. Sending a string: ***Hello, World!**

::

   Data          : "Hello, World!"                     -> 48 65 6C 6C 6F 2C 20 57 6F 72 6C 64 21
   Header        : 00000000 00000000 00000000 00001101 -> 00 00 00 00 00 00 00 00 00 00 00 00 0D (No flags, length is 0x0D)
   Complete frame: 00 00 00 00 00 00 00 00 00 00 00 00 0D 48 65 6C 6C 6F 2C 20 57 6F 72 6C 64 21
   
   32         24         16                  0
   +----------+----------+-------------------+----------------------------+
   | 00000000 | 00000000 | 00000000 00001101 | 1001000 1100101 1101100... |
   +----------+----------+-------------------+----------------------------+

2. Sending an **error**.

::

   Data          : "Invalid hash!"                     -> 49 6E 76 61 6C 69 64 20 68 61 73 68 21
   Header        : 10000000 00000000 00000000 00001101 -> 80 00 00 00 00 00 00 00 00 00 00 00 0D (Error flag, length is 0x0D)
   Complete frame: 80 00 00 00 00 00 00 00 00 00 00 00 0D 49 6E 76 61 6C 69 64 20 68 61 73 68 21
   
   32         24         16                  0
   +----------+----------+-------------------+----------------------------+
   | 10000000 | 00000000 | 00000000 00001101 | 1001001 1101110 1110110... |
   +----------+----------+-------------------+----------------------------+
