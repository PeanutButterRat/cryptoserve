.. _custom_exercises:

.. |Client| replace:: :py:class:`Client <cryptoserve.messaging.client.Client>`
.. |expect| replace:: :py:meth:`expect <cryptoserve.messaging.client.Client.expect>`
.. |send| replace:: :py:meth:`send <cryptoserve.messaging.client.Client.send>`
.. |ExerciseError| replace:: :py:class:`ExerciseError <cryptoserve.types.errors.ExerciseError>`

Custom Exercises
================

Cryptoserve can also be easily extended to add your own exercises! The process is not too difficult overall,
but there are a couple of specifics that you should be aware of though.


Creating the Exercise
---------------------

To create a new exercise, simply create a new Python file with a descriptive name.

.. code-block:: shell

   vim your_custom_exercise.py  # Or use your preferred code-editor.

This file will house all the code that the exercise needs to run properly.


Implementing the Exercise
-------------------------

Inside your Python file, you are required to implement one function:

.. code-block:: python

   def your_custom_exercise(client: Client) -> None:
      pass

This function should receive one argument: an instance of the |Client| class, which is used to send
messages back and forth from the user. To be recognized by Cryptoserve as a valid exercise, the function header
**must use type hints**, return **None**, and the function name **must not be prefixed with an underscore** (i.e. it must be public).

.. note:: The name of your function will be converted from snakecase and used as the exercise name.


Receiving Data and Checking for Errors
--------------------------------------

The two methods you are probably most interested in are:

1. |expect| for receiving data.
2. |send| for sending data.

|expect| is used to read from the socket. It takes optional arguments for verifying the length of the data received
as well as an function that is used to verify or transform the received data in some way. For instance, let's say
you expected to receive a pair of bytes that are coprime for some purpose. You could accomplish that like so:

.. code-block:: python

   from math import gcd

   def verify_byte_pair_is_coprime(received_data: bytes):
      if gcd(data[0], data[1]) == 1:
         raise ExerciseError(
            error="short Pythonic error message",
            explanation="A longer English-style sentence or two about what the user did wrong.",
            hints=[
               "A list of hints to help guide the user to make corrections.",
               "It can be any number of strings.",
               "This argument can also be None if no hints are warranted."
            ]
         )

      return data

   data = client.expect(length=2, verifier=verify_byte_pair_is_coprime)
   # From this point on, you can assume data refers to a valid byte pair...

.. warning:: Because Cryptoserve is an asynchronous server, you must use the ``await`` keyword when calling (most) methods from the |Client| class!

Notice how the verifier function does not explicitly check the length of `data`. This is because the length of the bytes
passed to the function is checked before the verifier is called, so the length is guaranteed to be 2. If you need more complex
length-checking or want more explicit, you must place that logic in the verifier itself.

To stop the exercise due to an error, simply raise an instance of |ExerciseError|. There are also various subclasses with different names
but have the same functionality. Choose the one with the name that gives the most insight into what went wrong or make your own subclass!


Verifier Parameters
^^^^^^^^^^^^^^^^^^^

The verifier function is passed data from the server based on the names of its arguments.

1. ``received_data``: the actual bytes of the message.
2. ``server_flags``: the server flags byte of the message.
3. ``exercise_flags``: the server flags byte of the message.

In order for your verifier to be called with any of these parts, you must include that parameter with that exact name. Here are some examples:

.. code-block:: python

   # This verifier just receives the message data.
   def verifier(received_data):
      pass

   # This verifier just receives the exercise flags from the message.   
   def verifier(exercise_flags):
      pass

   # This verifier just receives the flags from the message.
   def verifier(server_flags, exercise_flags):
      pass

   # This verifier receives all parts of the message.
   def verifier(received_data, server_flags, exercise_flags):
      pass

   # This verifier wont receive any messsage data.
   def verifier():
      pass

This allows you to pick and choose what parts of a message are relevant for your purposes. For example, if you are expecting data that doens't
rely on any exercise flags, you don't need to include it in your verifier function.


Making You Exercise Available
-----------------------------

Once you have implemented (and tested) your exercise the only thing left to do is to drop it into the **exercises** folder.

.. code-block:: shell

   mv your_custom_exercise.py cryptoserve/src/exercises/your_custom_exercise.py

The next time the server restarts, Cryptoserve automatically scans this folder to locate all the exercise functions. This process is also recursive,
so feel free to change the directory structure and organize the folders as you see fit.
