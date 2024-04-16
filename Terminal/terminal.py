from dataclasses import dataclass
import os

from Questions.core import Question


@dataclass
class Terminal:

    def ask_question(self, question:Question):
        print(question.description)