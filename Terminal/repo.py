from dataclasses import dataclass
from injector import inject
from prompt_toolkit.history import FileHistory

from Commons.constants import HISTORY_PATH


@inject
@dataclass
class TerminalRepo:

    def __init__(self):
        self.history = FileHistory(HISTORY_PATH)

    def get_terminal_history(self):
        return self.history

    def reset_terminal_history(self):
        with open(self.history.filename, "w") as file:
            file.write("")
