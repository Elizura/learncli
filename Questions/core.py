from enum import Enum
from typing import Optional
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    level: int
    type: int
    question_number: int
    description: str
    command: str
    expected_output: str


class QuestionType(Enum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3
