from dataclasses import dataclass


@dataclass
class NoteDTO:
    filepath: str


@dataclass
class NoteWithContentDTO:
    note: NoteDTO
    content: str
