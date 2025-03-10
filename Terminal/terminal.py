from enum import Enum
import os
from dataclasses import dataclass
import subprocess
from injector import inject
from prompt_toolkit import *
from Commons.constants import HISTORY_PATH
from DB.repo import DBRepo
from Questions.core import Question, QuestionType
from Questions.repo import QuestionsRepo
from TUIStyles.style_provider import StyleProvider
from Terminal.fancy_zhs import get_prompt
from Terminal.intro_screen import introduce
from Terminal.repo import TerminalRepo
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
        if self.db_repo.is_first_run():
            self.db_repo.mark_as_run()
            introduce()
        level, question_number = self.db_repo.get_status()
        question = self.repo.get_question(level=level, question_number=question_number)
        quit = False
        while not quit:
            self.display_content(content=question.description)
            is_correct = False
            while not is_correct and not quit:
                submitted, cmd = self.handle_inputs()
                if cmd == Command.QUIT or cmd == "exit":
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
                    rerun = self.handle_terminal_commands(command=cmd)
                    if rerun:
                        self.display_content(content=question.description)

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
        if question.type == QuestionType.TYPE1:
            answered = self.execute_command_and_check(question.command, expected_output)
        elif question.type == QuestionType.TYPE2:
            answered = self.check_history_and_execute(expected_output)

        return answered


    def execute_command_and_check(self, command, expected_output):
        try:
            pipe = subprocess.Popen(command, cwd="/learncli", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = pipe.communicate()
            if pipe.returncode != 0:
                if stderr:
                    print(stderr.decode())
                return False
            output = stdout.decode().splitlines()
            return output == expected_output
        except Exception as e:
            print(f"Exception occurred: {e}")
            return False


    def check_history_and_execute(self, expected_output):
        with open(file=HISTORY_PATH, mode="r") as ans:
            content = ans.read().split("\n")
            last_cmd = [line.strip("+") for line in content if line.strip()][-1]
            pipe = os.popen(last_cmd)
            out = pipe.read()
            return out.splitlines() == expected_output

    def advance_to_next_question(self, level, question_number):
        self.db_repo.set_status(level=level, qno=question_number + 1)


    def handle_terminal_commands(self, command):
        if command.startswith('cd '):
            try:
                os.chdir(command.split(' ', 1)[1])
                return False
            except FileNotFoundError:
                print("Directory not found.")
                return False
            except IndexError:
                os.chdir(os.path.expanduser("~"))
                return False
        else:
            os.system(command)
            if command == 'clear':
                return True