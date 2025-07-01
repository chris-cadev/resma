
from abc import ABC
import os
from typing import Optional
from resma.annotate.interfaces.interactors import AnnotateConfigurationInteractor, AnnotateNoteRepositoryInteractor
from resma.shared.use_cases import Interactor


class NoteInteractor(Interactor, ABC):
    def __init__(self, *, notes_repo: AnnotateNoteRepositoryInteractor, config: AnnotateConfigurationInteractor):
        self.notes_repo = notes_repo
        self.config = config

    def get_note_directory(self, *, vault: Optional[str] = None):
        note_vault = vault or self.config.default_vault
        note_directory = self.config.vaults[note_vault]
        if not os.path.isabs(note_directory):
            return os.path.join(self.config.workspace, note_directory)
        return note_directory

    def get_note_filepath(self, *, name: Optional[str] = None, vault: Optional[str] = None):
        note_name = name or self.config.default_note_name
        note_directory = self.get_note_directory(vault=vault)
        return os.path.join(note_directory, f'{note_name}.md')
