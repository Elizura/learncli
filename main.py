from injector import Injector, Module, singleton
from Check.checks import Check
from Questions.core import Question
from Questions.repo import QuestionsRepo
from Terminal.terminal import Terminal


def main(repo:QuestionsRepo, ter:Terminal, check:Check):
    question:Question = repo.get_question(level=1, question_number=1)    
    question_number = 1

    while True:
        ter.ask_question(question=question)
        is_correct = check.check_answer(question=question)        
        if is_correct:            
            question_number += 1
            question:Question = repo.get_question(question_number=question_number)

class AppModule(Module):
    def configure(self, binder):
        binder.bind(QuestionsRepo, to=QuestionsRepo, scope=singleton)
        binder.bind(Terminal, to=Terminal, scope=singleton)
        binder.bind(Check, to=Check, scope=singleton)

if __name__ == "__main__":
    injector = Injector([AppModule()])
    qrepo = injector.get(QuestionsRepo)
    terminal = injector.get(Terminal)
    check = injector.get(Check)       
    main(qrepo, terminal, check)