from dataclasses import dataclass
from injector import inject

from Questions.core import Question


@inject
@dataclass
class Terminal:

    def ask_question(self, question:Question):
        print(question.description)