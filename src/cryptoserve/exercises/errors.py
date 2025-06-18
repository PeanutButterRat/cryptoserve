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
