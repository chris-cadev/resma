

from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.interactors import AnnotateConfigInteractor, AnnotateNoteEditorGateway, AnnotateNoteRepositoryInteractor
from resma.annotate.use_cases.create_note.interactors import NoteInteractor


class EditNoteInteractor(NoteInteractor):
    def __init__(self, *, repository: AnnotateNoteRepositoryInteractor, config: AnnotateConfigInteractor, gateway: AnnotateNoteEditorGateway):
        super().__init__(notes_repo=repository, config=config)
        self.gateway = gateway

    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None) -> Note:
        filepath = self.get_note_filepath(name=name, vault=vault)
        dto = self.notes_repo.get(filepath=filepath)
        self.gateway.open_editor(filepath=dto.filepath)
        return dto
