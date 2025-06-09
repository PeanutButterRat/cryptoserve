import textwrap
from inspect import getmembers, isfunction

import cryptoserve.exercises

LINE_WIDTH = 70
PADDING = " " * 3
CONTENT_WIDTH = LINE_WIDTH - (len(PADDING) + 1) * 2
DOCUMENTATION_LINK = "https://cryptoserve.readthedocs.io/"


def center(sentence: str) -> str:
    """Centers the given sentence with vertical bars (|) and spacing on either side."""
    return f"|{PADDING}{sentence.center(CONTENT_WIDTH)}{PADDING}|"


def wrap(section: str) -> str:
    """Wraps a section of text and adds vertical bars (|) and padding to each wrapped line."""
    sentence_length = LINE_WIDTH - (len(PADDING) + 1) * 2
    sentences = textwrap.wrap(section, sentence_length)
    sentences = map(center, sentences)
    return "\n".join(sentences)


# Separation bar that looks like "+==========+".
horizontal_bar = "+" + "=" * (LINE_WIDTH - 2) + "+"

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

# Blank line with bars at the ends used for spacing.
spacing = center("")

numbered_exercise_names = []
EXERCISES = []

for i, (name, exercise) in enumerate(getmembers(cryptoserve.exercises, isfunction)):
    exercise_converted_from_snakecase = name.replace("_", " ").title()
    number = f"{i:<1}. "
    numbered_line = f"{number}{exercise_converted_from_snakecase.ljust(CONTENT_WIDTH - len(number))}"
    formatted_line = center(numbered_line)
    numbered_exercise_names.append(formatted_line)
    EXERCISES.append(exercise)


sections = [
    horizontal_bar,
    center("Welcome to Cryptoserve!"),
    center(DOCUMENTATION_LINK),
    horizontal_bar,
    spacing,
    wrap(project_description),
    spacing,
    center("~~~"),
    spacing,
    wrap(usage_directions),
    spacing,
    horizontal_bar,
    center("Available Exercises:"),
    horizontal_bar,
    spacing,
    *numbered_exercise_names,
    spacing,
    horizontal_bar,
]

GREETING = "\n".join(sections)
