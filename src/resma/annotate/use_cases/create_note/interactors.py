from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.use_cases.note.interactors import NoteInteractor


class CreateNoteInteractor(NoteInteractor):
    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None) -> Note:
        filepath = self.get_note_filepath(name=name, vault=vault)
        note = Note.create(filepath=filepath)
        self.notes_repo.create(filepath=filepath)
        return note
