.. _connecting:

Connecting to the Server
========================

In order to connect to a server running Cryptoserve, you must have some level of understanding of raw TCP-sockets.
Fortunately, sockets are language-agnostic so you can use any programming language you are comfortable with in order to interact
with Cryptoserve. The following page highlights how to connect and interact with the server in Python, but the
concepts can be further applied to any general-purpose programming language.

This is just a simple example on how to use Cryptoserve. You can find more robust starter-code examples to use (in multiple langauges) `here <https://github.com/PeanutButterRat/cryptoserve/tree/main/clients>`_.

.. note:: This assumes you are familiar with the way Cryptoserve handles messages. For a more in-depth view, see :ref:`protocol`.


Opening a Socket
----------------

Cryptoserve speaks plain TCP, so any socket API will do. You can use the standard ``socket`` module in Python to connect synchronously

.. code-block:: python

   import socket

   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.connect(("cryptoserve.example.com", 5050))

.. note:: The default port Cryptoserve uses is **5050**, but be sure to reach out to your instructor to clarify which port to connect to.


Initial Greeting
----------------

After the normal handshake completes, the server immediately sends a greeting that contains the available
exercises to run. This data should be interpreted as a string and printed to the console.


.. code-block:: python

   def read(sock: socket.socket):
      header = sock.recv(4)                     # Read the header (always 4 bytes).
      length = int.from_bytes(header) & 0xFFFF  # Extract the length from the header's last two bytes.
      data = sock.recv(length)                  # Read the corresponding data.
      return data
   
   greeting = read(sock)
   print(greeting.decode())


Starting an Exercise
--------------------

To select an exercise, send the exercise name as an UTF-8 string, framed using the Cryptoserve protocol.

.. code-block:: python

   def send(sock: socket.socket, data: bytes):
      header = len(data).to_bytes(4)  # Create the header.
      sock.sendall(header + data)     # Send the header concatentated with the actual data.

   send(sock, "Simple Hash".encode())

Then read the server's response to ensure you started the correct exercise.

.. code-block:: python

   confirmation = read(sock)
   print(greeting.confirmation())


Example Code
------------

Here is the complete code for what we have written:


.. code-block:: python

   import socket


   def send(sock: socket.socket, data: bytes):
      header = len(data).to_bytes(2)            # Create the header.
      sock.sendall(header + data)               # Send the header concatentated with the actual data.


   def read(sock: socket.socket):
      header = sock.recv(4)                     # Read the header (always 4 bytes).
      length = int.from_bytes(header) & 0xFFFF  # Extract the length from the header's last two bytes.
      data = sock.recv(length)                  # Read the corresponding data.
      return data


   def main():
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect(("cryptoserve.example.com", 5050))

      # Read the initial greeting.
      greeting = read(sock)
      print(greeting.decode())

      # Start an exercise.
      send(sock, "Simple Hash".encode())

      # Add steps to complete Exercise 1 here...


   # Import guard (good practice, but not necessary).
   if __name__ == "__main__":
      main()


Completing an Exercise
----------------------

Please refer to :ref:`listing` to see how to complete a specific exercise. In general,
here are some tips that you might find useful in your work:

- Before using data received from the server, check to see if the **error flag** is set. If so, print out the message and terminate your program.
- Carefully read the instructions for a particular exercise before attempting to complete it.
- Solve the exercise incrementally. Don't write a bunch of code all at once as this is difficult to debug. Instead, ensure each message exchange is working properly before moving on to the next.
- If you are really stuck, it might be helpful to refer to Cryptoserve's source code for clarification (it *is* an open-source project, after all).
- Most importantly, don't be embarrassed to ask for help!

Extra Resources
---------------

- `Python socket Module Documentation <https://docs.python.org/3/library/socket.html>`_
