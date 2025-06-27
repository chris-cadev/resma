from abc import ABC, abstractmethod
from typing import Optional, Union

from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.dto import NoteDTO, NoteWithContentDTO, TemplateDTO


class AnnotateConfigInteractor(ABC):

    @property
    @abstractmethod
    def vaults(self) -> dict:
        pass

    @property
    @abstractmethod
    def default_note_name(self) -> str:
        pass

    @property
    @abstractmethod
    def default_vault(self) -> str:
        pass

    @property
    @abstractmethod
    def editor_cmd(self) -> str:
        pass

    @property
    @abstractmethod
    def workspace(self) -> str:
        pass

    @property
    @abstractmethod
    def templates_dir(self) -> str:
        pass

    @property
    @abstractmethod
    def templates(self) -> str:
        pass


class AnnotateNoteRepositoryInteractor(ABC):
    @abstractmethod
    def create(self, *, filepath: str, content: Union[str, None]) -> NoteWithContentDTO:
        pass

    @abstractmethod
    def append(self, *, filepath: str, content: str) -> NoteWithContentDTO:
        pass

    @abstractmethod
    def get(self, *, filepath: str) -> Union[NoteWithContentDTO, None]:
        pass


class AnnotateTemplateRepositoryInteractor(ABC):
    @abstractmethod
    def get(self, *, filepath: str) -> TemplateDTO:
        pass


class AnnotateTemplateNoteInteractor(ABC):
    @abstractmethod
    def evaluate_template(self, *, template: TemplateDTO, note: Optional[Note], meta: Optional[dict]) -> NoteWithContentDTO:
        pass

class AnnotateNoteEditorGateway(ABC):
    @abstractmethod
    def open_editor(self, *, filepath: str) -> bool:
        pass

class CreateNoteController(ABC):
    @abstractmethod
    def create_note(self, *, name: str, vault_name: Optional[str]) -> NoteDTO:
        pass


class CreateTemplateNoteController(ABC):
    @abstractmethod
    def create_note(self, *, name: str, vault_name: Optional[str], template: Optional[str], meta: Optional[dict]) -> NoteDTO:
        pass


class EditNoteController(ABC):
    @abstractmethod
    def edit_note(self, *, name: str, vault_name: Optional[str]) -> NoteWithContentDTO:
        pass
