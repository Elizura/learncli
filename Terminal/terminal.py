import os
from dataclasses import dataclass
from injector import inject
from prompt_toolkit import *
from Questions.core import Question
from Questions.repo import QuestionsRepo
from Terminal.repo import TerminalRepo
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import clear



@dataclass
class Terminal:

    @inject
    def __init__(self, terminal_repo: TerminalRepo, repo: QuestionsRepo):
        self.terminal_repo = terminal_repo        
        self.repo = repo 
        self.custom_style = Style.from_dict({
            'prompt': 'ansicyan',
        })
       

    def run(self):
        question_number = 1
        question = self.repo.get_question(level=1, question_number=1)
        while True:
            clear()
            print(question.description)
            is_correct = False
            while not is_correct:
                submitted, cmd = self.handle_inputs()
                if submitted:
                    is_correct = self.check_answer(question=question)
                    if is_correct:
                        print("CORRECTUMUNDO")
                        question_number += 1
                        question = self.repo.get_question(question_number=question_number)
                else:
                    os.system(cmd)

    def handle_inputs(self):        
        inp = prompt(
                '> ',
                history=self.terminal_repo.get_terminal_history(),
                multiline=False,
                enable_system_prompt=True,
                style=self.custom_style
            )        
        if inp.lower() == 'submit':
            return True, ''
        else:
            return False, inp
        

    def check_answer(self, question:Question):
        expected_output = question.expected_output
        command = question.command
        answered = False                                     
        pipe = os.popen(command)            
        out = pipe.read()
        pipe.close()  
        answered = out.splitlines() == expected_output        
        return answered