.. _custom_exercises:

Custom Exercises
================

Cryptoserve can be easily extended to add your own exercises. Here is a short list of steps to do so:


1. **Create a Python file**.
2. **Implement your exercise** as a Python function with the following signature:

.. code-block:: python

   def your_custom_exercise(client: Client):
      pass

.. note:: Please refer to the internal documentation for how to use the Client class.

.. note:: The name of your function will be converted from snakecase and used as the exercise name. 

3. **Restart Cryptoserve**. Future students should now be able to connect to the server and select your exercises from the avialble list.
4. **Document your exercise**. Please see Contributing for how to document your exercise.
