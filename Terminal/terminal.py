from enum import Enum
import os
from dataclasses import dataclass
from injector import inject
from prompt_toolkit import *
from Commons.constants import HISTORY_PATH
from DB.repo import DBRepo
from Questions.core import Question, QuestionType
from Questions.repo import QuestionsRepo
from TUIStyles.style_provider import StyleProvider
from Terminal.fancy_zhs import get_prompt
from Terminal.repo import TerminalRepo
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from pygments.lexers.shell import BashLexer
from prompt_toolkit.lexers import PygmentsLexer


class Command(Enum):
    QUIT = 1
    SUBMIT = 2


@dataclass
class Terminal:

    @inject
    def __init__(
        self, terminal_repo: TerminalRepo, repo: QuestionsRepo, db_repo: DBRepo, style_provider:StyleProvider
    ):
        self.db_repo = db_repo
        self.terminal_repo = terminal_repo
        self.repo = repo
        self.style_provider = style_provider

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
                        self.advance_to_next_question(level, question_number)
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
                get_prompt,
                style=self.style_provider.get_fancy_zhs_style(),
                history=self.terminal_repo.get_terminal_history(),
                multiline=False,
                enable_system_prompt=True,                
                key_bindings=kb,
                lexer=PygmentsLexer(BashLexer),
            )

            if inp == Command.SUBMIT:
                return True, _

            return False, inp

        except KeyboardInterrupt:
            return _, Command.QUIT

    def check_answer(self, question: Question):
        expected_output = question.expected_output
        answered = False
        if question.question_number == 6 or question.question_number == 4:
            return True
        if question.type == QuestionType.TYPE1:
            answered = self.execute_command_and_check(question.command, expected_output)
        elif question.type == QuestionType.TYPE2:
            answered = self.check_history_and_execute(expected_output)

        return answered

    def execute_command_and_check(self, command, expected_output):
        pipe = os.popen(command)
        out = pipe.read()
        pipe.close()
        return out.splitlines() == expected_output

    def check_history_and_execute(self, expected_output):
        with open(file=HISTORY_PATH, mode="r") as ans:
            content = ans.read().split("\n")
            last_cmd = [line.strip("+") for line in content if line.strip()][-1]
            pipe = os.popen(last_cmd)
            out = pipe.read()
            print(out, expected_output)
            return out.splitlines() == expected_output

    def advance_to_next_question(self, level, question_number):
        self.db_repo.set_status(level=level, qno=question_number + 1)
