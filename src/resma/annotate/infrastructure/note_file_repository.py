import os
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.dto import NoteWithContentDTO
from resma.annotate.interfaces.interactors import AnnotateNoteRepositoryInteractor


class NoteFilesRepository(AnnotateNoteRepositoryInteractor):
    def create(self, filepath: str, content: str = ''):
        if os.path.exists(filepath):
            raise SystemError(f'Note already exists at {filepath}')
        note_directory = os.path.dirname(filepath)
        if not os.path.exists(note_directory):
            os.makedirs(note_directory)
        with open(filepath, 'w') as n:
            n.write(content)
            return NoteWithContentDTO(
                filepath=filepath,
                content=content,
            )
        return None

    def append(self, *, filepath: str, content: str):
        if not content:
            return self.get(filepath=filepath)
        with open(filepath, 'a') as n:
            n.write(content)
            return NoteWithContentDTO(
                filepath=filepath,
                content=content
            )
        raise SystemError(f'Failed to append to file: {note.filepath}')

    def get(self, *, filepath):
        if not os.path.exists(filepath):
            raise ValueError(f"Note {filepath} does not exist")
        with open(filepath) as n:
            content = n.read()
            return NoteWithContentDTO(
                filepath=filepath,
                content=content
            )
