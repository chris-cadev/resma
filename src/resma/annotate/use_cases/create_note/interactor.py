from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.interactors import AnnotateEnvInteractor, AnnotateNoteRepositoryInteractor
from resma.shared.use_cases import Interactor


class CreateNoteInteractor(Interactor):
    def __init__(self, repository: AnnotateNoteRepositoryInteractor, env: AnnotateEnvInteractor):
        self.repository = repository
        self.env = env

    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None, template: Optional[str] = None) -> Note:
        note_name = name
        if not note_name:
            note_name = self.env.default_note_name
        note_vault = vault
        if not note_vault:
            note_vault = self.env.default_vault
        note_directory = self.env.vaults[note_vault]
        note = self.repository.create(
            Note.create(
                filepath=f"{note_directory}/{note_name}.md"
            )
        )
        return note
