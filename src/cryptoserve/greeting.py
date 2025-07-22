"""Welcome message for the server.

This module serves as a "greeting formatter" for Cryptoserve. It builds a nicely-formatted, colorful
string that is sent to users when they first connect. It relies on Rich to build the message with ANSI color codes.

The `Rich Color Reference <https://rich.readthedocs.io/en/stable/appendix/colors.html>`_ might be of some use.

"""

import os

import cryptoserve.exercises
from cryptoserve.exercises import load_exercises
from cryptoserve.messaging import prettify

DOCUMENTATION_LINK = "https://cryptoserve.readthedocs.io/"
LINE_WIDTH = 70

project_description = """Cryptoserve is server software that hosts a library 
of cryptography-related exercises, designed to help students learn a broad
range of cryptographic concepts through hands-on experimentation. Each
exercise defines a protocol in which Cryptoserve controls one side of
the interaction."""

project_description = project_description.replace("\n", "")

usage_directions = f"""As the end user, YOU are responsible for implementing
the other side of the exchange in order to complete the challenge. To
get started, please select from one of the available exercises listed
below. For more usage information, please refer to the official
documentation at {DOCUMENTATION_LINK}."""

usage_directions = usage_directions.replace("\n", "")

path = os.path.dirname(cryptoserve.exercises.__file__)

EXERCISES = []
numbered_exercise_names = []

for i, (name, exercise) in enumerate(load_exercises(path)):
    exercise_converted_from_snakecase = name.replace("_", " ").title()
    number = f"{i:<1}. "
    numbered_line = f"{number}{exercise_converted_from_snakecase}"
    numbered_exercise_names.append(numbered_line)
    EXERCISES.append((exercise_converted_from_snakecase, exercise))

numbered_exercise_names = "\n".join(numbered_exercise_names)

sections = [
    ("Welcome to Cryptoserve!", DOCUMENTATION_LINK, "green"),
    ("About", project_description, "dark_turquoise"),
    ("Usage", usage_directions, "dark_blue"),
    ("Available Exercises", numbered_exercise_names, "dark_orange3"),
]

GREETING = prettify(sections)
