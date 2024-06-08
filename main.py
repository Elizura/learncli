from injector import Injector, Module, singleton
from Check.checks import Check
from DB.repo import DBRepo
from Questions.repo import QuestionsRepo
from TUIStyles.style_provider import StyleProvider
from Terminal.repo import TerminalRepo
from Terminal.terminal import Terminal


class AppModule(Module):
    def configure(self, binder):
        binder.bind(QuestionsRepo, to=QuestionsRepo, scope=singleton)
        binder.bind(TerminalRepo, to=TerminalRepo, scope=singleton)
        binder.bind(DBRepo, to=DBRepo, scope=singleton)
        binder.bind(StyleProvider, to=StyleProvider, scope=singleton)


if __name__ == "__main__":
    injector = Injector([AppModule()])
    db_repo = injector.get(DBRepo)
    db_repo.get_status()
    terminal = injector.get(Terminal)
    
    terminal.run()
