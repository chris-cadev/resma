

from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.interactors import AnnotateConfigurationInteractor, AnnotateNoteRepositoryInteractor
from resma.annotate.use_cases.create_note.interactors import NoteInteractor
from resma.shared.infrastructure.interactors import NoteEditorGateway


class EditNoteInteractor(NoteInteractor):
    def __init__(self, *, repository: AnnotateNoteRepositoryInteractor, config: AnnotateConfigurationInteractor, editor: NoteEditorGateway):
        super().__init__(notes_repo=repository, config=config)
        self.editor = editor

    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None) -> Note:
        filepath = self.get_note_filepath(name=name, vault=vault)
        dto = self.notes_repo.get(filepath=filepath)
        self.editor.open(filepath=dto.filepath)
        return dto
