from dataclasses import dataclass


@dataclass
class NoteDTO:
    filepath: str


@dataclass
class NoteWithContentDTO:
    filepath: str
    content: str


@dataclass
class TemplateDTO:
    filepath: str
    content: str
