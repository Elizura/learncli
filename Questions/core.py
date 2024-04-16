from typing import Optional
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    level: int
    question_number: int
    description: str    
    command: str
    expected_output: str