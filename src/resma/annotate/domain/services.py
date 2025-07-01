import os
from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.interactors import AnnotateConfigurationInteractor, AnnotateNoteRepositoryInteractor


class NotesService:
    def __init__(self, env: AnnotateConfigurationInteractor, repository: AnnotateNoteRepositoryInteractor):
        self.env = env
        self.repository = repository

    def create_note(self, content: str, name: Optional[str] = None, vault: Optional[str] = None) -> Note:
        selected_vault = vault or self.env.default_vault
        note_directory = self.env.vaults.get(selected_vault)

        if not note_directory:
            raise ValueError(f"Vault '{selected_vault}' not found in config.")

        note_name = name or self.env.default_note_name
        filepath = os.path.join(note_directory, f"{note_name}.md")

        return self.repository.create(
            filepath=Note.create(filepath=filepath),
            content=content,
        )
