import os
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.dto import NoteWithContentDTO
from resma.annotate.interfaces.interactors import AnnotateNoteRepositoryInteractor


class FilesystemNoteRepository(AnnotateNoteRepositoryInteractor):
    def create(self, note: Note, content: str = ''):
        if os.path.exists(note.filepath):
            return note
        note_directory = os.path.dirname(note.filepath)
        if not os.path.exists(note_directory):
            os.makedirs(note_directory)
        with open(note.filepath, 'w') as n:
            n.write(content)
            return note
        return None

    def get(self, *, filepath):
        if not os.path.exists(filepath):
            raise ValueError(f"Note file {filepath} does not exist")
        with open(filepath) as n:
            content = n.read()
            return NoteWithContentDTO(
                note=Note.create(filepath=filepath),
                content=content
            )
