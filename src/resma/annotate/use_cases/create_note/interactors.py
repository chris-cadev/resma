from abc import ABC
from typing import Optional
from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.interactors import AnnotateConfigInteractor, AnnotateNoteEditorGateway, AnnotateNoteRepositoryInteractor
from resma.shared.use_cases import Interactor


class NoteInteractor(Interactor, ABC):
    def __init__(self, *, repository: AnnotateNoteRepositoryInteractor, config: AnnotateConfigInteractor):
        self.repository = repository
        self.config = config

    def get_note_filepath(self, *, name: Optional[str] = None, vault: Optional[str] = None):
        note_name = name
        if not note_name:
            note_name = self.config.default_note_name
        note_vault = vault
        if not note_vault:
            note_vault = self.config.default_vault
        note_directory = self.config.vaults[note_vault]
        return f"{note_directory}/{note_name}.md"


class CreateNoteInteractor(NoteInteractor):
    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None, template: Optional[str] = None) -> Note:
        filepath = self.get_note_filepath(name=name, vault=vault)
        note = self.repository.create(
            Note.create(filepath=filepath)
        )
        return note


class EditNoteInteractor(NoteInteractor):
    def __init__(self, *, repository: AnnotateNoteRepositoryInteractor, config: AnnotateConfigInteractor, gateway: AnnotateNoteEditorGateway):
        super().__init__(repository=repository, config=config)
        self.gateway = gateway

    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None) -> Note:
        filepath = self.get_note_filepath(name=name, vault=vault)
        dto =self.repository.get(filepath=filepath)
        self.gateway.open_editor(filepath=dto.note.filepath)
        return dto
