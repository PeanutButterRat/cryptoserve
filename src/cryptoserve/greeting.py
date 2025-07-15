import os

import cryptoserve.exercises
from cryptoserve.exercises import load_exercises
from cryptoserve.messaging.text_menu import TextMenu

DOCUMENTATION_LINK = "https://cryptoserve.readthedocs.io/"
LINE_WIDTH = 70

project_description = """Cryptoserve is server software that hosts a library of 
cryptography-related exercises, designed to help students learn a broad
range of cryptographic concepts through hands-on experimentation. Each
exercise defines a protocol in which Cryptoserve controls one side of
the interaction.
"""

usage_directions = f"""As the end user, YOU are responsible for implementing
the other side of the exchange in order to complete the challenge. To
get started, please select from one of the available exercises listed
below. For more usage information, please refer to the official
documentation at {DOCUMENTATION_LINK}."""

menu = TextMenu(max_width=75)
menu.add_section("Welcome to Cryptoserve!", "greeting")
menu.greeting.add_line(DOCUMENTATION_LINK)

menu.add_section("About")
menu.about.add_line(project_description)

menu.add_section("Usage")
menu.usage.add_line(usage_directions)


menu.add_section("Available Exercises", "exercises")
numbered_exercise_names = []
EXERCISES = []

path = os.path.dirname(cryptoserve.exercises.__file__)


for i, (name, exercise) in enumerate(load_exercises(path)):
    exercise_converted_from_snakecase = name.replace("_", " ").title()
    number = f"{i:<1}. "
    numbered_line = f"{number}{exercise_converted_from_snakecase}"
    menu.exercises.add_line(numbered_line)
    EXERCISES.append((exercise_converted_from_snakecase, exercise))

GREETING = str(menu)
