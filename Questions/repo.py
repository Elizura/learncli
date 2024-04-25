from dataclasses import dataclass
from injector import inject
import yaml
from Commons.constants import QUESTIONS_SOURCE_PATH
from Questions.core import Question, QuestionType


@inject
@dataclass
class QuestionsRepo:

    def add_question(self) -> None:
        pass

    def load_db(self) -> None:
        questions = []
        with open(QUESTIONS_SOURCE_PATH, "r") as file:
            data = yaml.safe_load(file)
            for question_info in data:
                id = question_info["id"]
                level = question_info["level"]
                question_number = question_info["question_number"]
                description = question_info["description"]
                command = question_info["command"]
                expected_output = question_info["expected_output"]
                question_type = QuestionType(question_info["type"])
                question = Question(
                    id=id,
                    command=command,
                    description=description,
                    expected_output=expected_output,
                    level=level,
                    question_number=question_number,
                    type=question_type,
                )
                questions.append(question)
        return questions

    def get_questions(self):
        pass

    def get_question(self, **kwargs) -> Question:
        questions = self.load_db()
        filtered_questions = questions

        for key, value in kwargs.items():
            filtered_questions = [
                q for q in filtered_questions if getattr(q, key) == value
            ]

        if filtered_questions:
            return filtered_questions[0]
        else:
            return None
