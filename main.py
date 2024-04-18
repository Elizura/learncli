from injector import Injector, Module, singleton
from Check.checks import Check
from Questions.repo import QuestionsRepo
from Terminal.repo import TerminalRepo
from Terminal.terminal import Terminal


class AppModule(Module):
    def configure(self, binder):
        binder.bind(QuestionsRepo, to=QuestionsRepo, scope=singleton)
        binder.bind(TerminalRepo, to=TerminalRepo, scope=singleton)        


if __name__ == "__main__":
    injector = Injector([AppModule()])    
    terminal = injector.get(Terminal)
    terminal.run()
