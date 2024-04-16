import os
from dataclasses import dataclass

from Questions.core import Question


@dataclass
class Check:

    def __init__(self) -> None:
        pass

    def check_answer(self, question:Question):
        expected_line = question.expected_output
        command = question.command
        answered = False             
        while not answered:
            user_input = input()
            if user_input == "submit":
                pipe = os.popen(command)            
                out = pipe.read()
                pipe.close()  
                answered = out.splitlines() == expected_line
            else:
                os.system(user_input)
        
        return True