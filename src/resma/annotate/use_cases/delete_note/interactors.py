

from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.use_cases.create_note.interactors import NoteInteractor

class DeleteNoteInteractor(NoteInteractor):
    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None) -> Note:
        filepath = self.get_note_filepath(name=name, vault=vault)
        dto = self.notes_repo.delete(filepath=filepath)
        return dto
