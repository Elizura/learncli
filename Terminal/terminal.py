import argparse
import os
from dataclasses import dataclass
from injector import inject
from prompt_toolkit import *
from DB.repo import DBRepo
from Questions.core import Question
from Questions.repo import QuestionsRepo
from Terminal.repo import TerminalRepo
from prompt_toolkit.styles import Style


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

    def display_content(self, question:Question):
        os.system('cls' if os.name == 'nt' else 'clear')
        question = question.description + "\n" + question.description + question.description
        lines = question.split('\n')
        max_length = max(len(line) for line in lines)
        
        print("╔" + "═" * (max_length + 4) + "╗")
                
        for line in lines:
            padding = max_length - len(line)
            print("║  " + line + " " * padding + "  ║")
                
        print("╚" + "═" * (max_length + 4) + "╝")

    def run(self):        
        level, question_number = self.db_repo.get_status()
        question = self.repo.get_question(level=level, question_number=question_number)
        while True:                        
            self.display_content(question=question)
            is_correct = False
            while not is_correct:
                submitted, cmd = self.handle_inputs()
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
        inp = prompt(
            "> ",
            history=self.terminal_repo.get_terminal_history(),
            multiline=False,
            enable_system_prompt=True,
            style=self.custom_style,
        )
        if inp.lower() == "submit":
            return True, ""
        else:
            return False, inp

    def check_answer(self, question: Question):
        expected_output = question.expected_output
        command = question.command
        answered = False
        pipe = os.popen(command)
        out = pipe.read()
        pipe.close()
        answered = out.splitlines() == expected_output
        return answered
