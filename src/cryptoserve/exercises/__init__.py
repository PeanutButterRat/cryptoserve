import importlib
import inspect
import os
from typing import get_type_hints

from cryptoserve.messaging.client import Client


def load_exercises(directory: str) -> list[tuple[str, callable]]:
    """
    Load Cryptoserve exercises from a directory.

    This method recursively searches through a directory for Python files to find functions that look like
    Cryptoserve exercises. The file must end with the **.py** file extension but doesn't have to be in a folder
    with the standard Python package structure.

    Valid exercise functions have two requirements:

    1. The function must **not be private** (i.e. it's name doesn't start with and underscore).
    2. The function must have the following signature specified with type hints: **(Client) -> None**

    Args:
        directory: The directory path to recursively search

    Returns:
        list[tuple[str, callable]]: A list of (exercise name, function) tuples for valid exercise functions.
    """
    exercises = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)

                try:
                    spec = importlib.util.spec_from_file_location("exercises", filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                except Exception:
                    continue

                for name, member in inspect.getmembers(module, inspect.isfunction):
                    if not name.startswith("_") and _has_exercise_signature(member):
                        exercises.append((name, member))

    return exercises


def _has_exercise_signature(function: callable):
    """
    Check if the callable object has the correct signature to be considered a Cryptoserve exercise.

    Returns True if the function name is not prefixed with an underscore (_) and has the signature **(Client) -> None**.
    The function must use type hints in order to be recognized as a proper exercise.

    Example: ``def my_exercise(client: Client) -> None:``

    Args:
        function (callable): The function object to test.

    Returns:
        bool: True if the function matches all the criteria, False otherwise.
    """
    signature = inspect.signature(function)
    hints = get_type_hints(function)
    parameters = list(signature.parameters.values())

    return (
        len(parameters) == 1
        and hints.get(parameters[0].name) is Client
        and hints.get("return") is None
    )
