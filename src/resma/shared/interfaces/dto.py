
from dataclasses import dataclass
from typing import Literal


@dataclass
class FileDTO:
    filepath: str

@dataclass
class TextFileWithContentDTO:
    filepath: str
    content: str

Mode = Literal['override', 'append']

@dataclass
class EvaluatedTemplateDTO:
    filepath: str
    content: str
    mode: Mode
