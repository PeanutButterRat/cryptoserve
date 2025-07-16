import json
from typing import List, Optional

from cryptoserve.messaging.printing import prettify


class ExerciseError(Exception):
    def __init__(
        self, error: str = "", explanation: str = "", hints: Optional[List[str]] = None
    ):
        super().__init__(error)
        self.explanation = explanation
        self.hints = hints or []

    def prettify(self):
        error = f"{type(self).__name__}: {self}"
        explanation = self.explanation if self.explanation else "None"
        hints = "\n".join([f"• {hint}" for hint in self.hints])

        sections = [
            ("Error", error, "indian_red"),
            ("Explanation", explanation, "green"),
            ("Hints", hints, "yellow"),
        ]

        if not hints:
            sections.pop()

        error = prettify(sections)

        return error


class InvalidPaddingError(ExerciseError):
    pass


class InvalidLengthError(ExerciseError):
    pass


class DataMismatchError(ExerciseError):
    pass


class DataTransmissionError(ExerciseError):
    pass


class ClientTimeoutError(ExerciseError):
    pass


class InvalidParameterError(ExerciseError):
    pass
