
from abc import ABC
import os
from typing import Optional
from resma.annotate.interfaces.interactors import AnnotateConfigInteractor, AnnotateNoteRepositoryInteractor
from resma.shared.use_cases import Interactor


class NoteInteractor(Interactor, ABC):
    def __init__(self, *, notes_repo: AnnotateNoteRepositoryInteractor, config: AnnotateConfigInteractor):
        self.notes_repo = notes_repo
        self.config = config

    def get_note_filepath(self, *, name: Optional[str] = None, vault: Optional[str] = None):
        note_name = name
        if not note_name:
            note_name = self.config.default_note_name
        note_vault = vault
        if not note_vault:
            note_vault = self.config.default_vault
        note_directory = self.config.vaults[note_vault]
        if not os.path.isabs(note_directory):
            return os.path.join(self.config.workspace, note_directory, f'{note_name}.md')
        return os.path.join(note_directory, f'{note_name}.md')
