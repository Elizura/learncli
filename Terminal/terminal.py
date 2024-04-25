import argparse
from enum import Enum
import os
from dataclasses import dataclass
from injector import inject
from prompt_toolkit import *
from Commons.constants import ANSWER_SUBMISSION_PATH
from DB.repo import DBRepo
from Questions.core import Question, QuestionType
from Questions.repo import QuestionsRepo
from Terminal.repo import TerminalRepo
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys


class Command(Enum):
    QUIT = 1
    SUBMIT = 2


@dataclass
class Terminal:

    @inject
    def __init__(
        self, terminal_repo: TerminalRepo, repo: QuestionsRepo, db_repo: DBRepo
    ):
        self.db_repo = db_repo
        self.terminal_repo = terminal_repo
        self.repo = repo
        self.custom_style = Style.from_dict(
            {
                "prompt": "ansicyan",
            }
        )

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def display_content(self, content):
        self.clear_screen()
        lines = content.split("\n")
        max_length = max(len(line) for line in lines)

        print("╔" + "═" * (max_length + 4) + "╗")

        for line in lines:
            padding = max_length - len(line)
            print("║  " + line + " " * padding + "  ║")

        print("╚" + "═" * (max_length + 4) + "╝")

    def run(self):
        level, question_number = self.db_repo.get_status()
        question = self.repo.get_question(level=level, question_number=question_number)
        quit = False
        while not quit:
            self.display_content(content=question.description)
            is_correct = False
            while not is_correct and not quit:
                submitted, cmd = self.handle_inputs()
                if cmd == Command.QUIT:
                    self.clear_screen()
                    quit = True
                    break
                if submitted:
                    is_correct = self.check_answer(question=question)
                    if is_correct:
                        self.db_repo.set_status(level=level, qno=question_number + 1)
                        level, question_number = self.db_repo.get_status()
                        question = self.repo.get_question(
                            level=level, question_number=question_number
                        )
                else:
                    os.system(cmd)

    def handle_inputs(self):
        kb = KeyBindings()

        @kb.add("c-s")
        def _(event):
            event.app.exit(result=Command.SUBMIT)

        try:
            inp = prompt(
                "> ",
                history=self.terminal_repo.get_terminal_history(),
                multiline=False,
                enable_system_prompt=True,
                style=self.custom_style,
                key_bindings=kb,
            )

            if inp == Command.SUBMIT:
                return True, _

            return False, inp

        except KeyboardInterrupt:
            return _, Command.QUIT

    def check_answer(self, question: Question):
        expected_output = question.expected_output
        command = question.command
        answered = False
        pipe = os.popen(command)
        out = pipe.read()
        if question.question_number == 6:
            return True
        if question.type == QuestionType.TYPE1:
            pipe.close()
            print("out>>", out.splitlines(), "the expected>>", expected_output)
            answered = out.splitlines() == expected_output

        elif question.type == QuestionType.TYPE2:
            with open(file=ANSWER_SUBMISSION_PATH, mode="r") as ans:
                content = ans.read().split("\n")
                ans = [line.strip() for line in content if line.strip()]
                answered = ans == expected_output

        return answered
