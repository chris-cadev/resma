from abc import ABC, abstractmethod
from typing import Optional, Union

from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.dto import TemplateDTO
from resma.shared.interfaces.dto import EvaluatedTemplateDTO, FileDTO, TextFileWithContentDTO
from resma.shared.interfaces.interactors import ConfigurationInteractor


class AnnotateConfigurationInteractor(ConfigurationInteractor, ABC):
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
    def templates_dir(self) -> str:
        pass

    @property
    @abstractmethod
    def templates(self) -> str:
        pass


class AnnotateNoteRepositoryInteractor(ABC):
    @abstractmethod
    def create(self, *, filepath: str, content: Union[str, None]) -> TextFileWithContentDTO:
        pass

    @abstractmethod
    def append(self, *, filepath: str, content: str) -> TextFileWithContentDTO:
        pass

    @abstractmethod
    def get(self, *, filepath: str) -> Union[TextFileWithContentDTO, None]:
        pass


class TemplateRepositoryInteractor(ABC):
    @abstractmethod
    def get(self, *, filepath: str) -> TemplateDTO:
        pass


class TemplateNoteInteractor(ABC):
    @abstractmethod
    def evaluate_template(self, *, template: TemplateDTO, note: Optional[Note], meta: Optional[dict]) -> EvaluatedTemplateDTO:
        pass


class NoteEditorGateway(ABC):
    @abstractmethod
    def open(self, *, filepath: str) -> bool:
        pass

class CreateNoteController(ABC):
    @abstractmethod
    def create_note(self, *, name: str, vault_name: Optional[str]) -> FileDTO:
        pass


class CreateTemplateNoteInteractor(ABC):
    @abstractmethod
    def create_note(self, *, name: str, vault_name: Optional[str], template: Optional[str], meta: Optional[dict]) -> FileDTO:
        pass


class EditNoteController(ABC):
    @abstractmethod
    def edit_note(self, *, name: str, vault_name: Optional[str]) -> TextFileWithContentDTO:
        pass
