import json
from typing import List, Optional


class ExerciseError(Exception):
    def __init__(
        self, error: str = "", explanation: str = "", hints: Optional[List[str]] = None
    ):
        super().__init__(error)
        self.explanation = explanation
        self.hints = hints or []

    def json(self):
        dictionary = {
            "error": f"{type(self).__name__}: {self}",
            "explanation": self.explanation,
            "hints": self.hints,
        }

        return json.dumps(dictionary)


class InvalidPaddingError(ExerciseError):
    def __init__(self, explanation: str = "", hints: Optional[List[str]] = None):
        error = "data has invalid padding"
        super().__init__(error, explanation, hints)


class InvalidLengthError(ExerciseError):
    def __init__(
        self,
        size_adjective: str = "large",
        explanation: str = "",
        hints: Optional[List[str]] = None,
    ):
        error = f"data is too {size_adjective}"
        super().__init__(error, explanation, hints)


class DataMismatchError(ExerciseError):
    def __init__(
        self,
        data_type: str = "data",
        explanation: str = "",
        hints: Optional[List[str]] = None,
    ):
        error = f"recived {data_type} does not match expected {data_type}"
        super().__init__(error, explanation, hints)


class DataTransmissionError(ExerciseError):
    pass
