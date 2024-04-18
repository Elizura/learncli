import os
from dataclasses import dataclass
from injector import inject
from Questions.core import Question


@inject
@dataclass
class Check:

    def __init__(self) -> None:
        pass

