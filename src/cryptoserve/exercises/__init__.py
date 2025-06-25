import importlib
import inspect
import os
from types import FunctionType
from typing import get_type_hints

from cryptoserve.messaging.client import Client


def load_exercises(directory: str):
    exercises = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)

                try:
                    spec = importlib.util.spec_from_file_location("exercises", filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                except Exception as e:
                    continue

                for name, member in inspect.getmembers(module, inspect.isfunction):
                    if not name.startswith("_") and _has_exercise_signature(member):
                        exercises.append((name, member))

    return exercises


def _has_exercise_signature(function: FunctionType):
    signature = inspect.signature(function)
    hints = get_type_hints(function)
    parameters = list(signature.parameters.values())

    return (
        len(parameters) == 1
        and hints.get(parameters[0].name) is Client
        and hints.get("return") is None
    )
