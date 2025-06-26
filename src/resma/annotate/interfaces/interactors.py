from abc import ABC, abstractmethod
from typing import Optional, Union

from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.dto import NoteDTO, NoteWithContentDTO


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


class AnnotateNoteRepositoryInteractor(ABC):
    @abstractmethod
    def create(self, *, note: Note, content: Union[str, None]) -> Union[Note, Exception]:
        pass

    @abstractmethod
    def get(self, *, filepath: str) -> Union[NoteWithContentDTO, None, Exception]:
        pass

    # @abstractmethod
    # def list(self, *, vault_name: Optional[str] = None) -> Union[list[Note], None, Exception]:
    #     pass

    # @abstractmethod
    # def delete(self, *, note_filepath: str) -> Union[bool, Exception]:
    #     pass


class AnnotateNoteEditorGateway(ABC):
    @abstractmethod
    def open_editor(self, *, filepath: str) -> Union[bool, Exception]:
        pass

class CreateNoteController(ABC):
    @abstractmethod
    def create_note(self, *, name: str, vault_name: Optional[str], template: Optional[str] = None) -> NoteDTO:
        pass


class EditNoteController(ABC):
    @abstractmethod
    def edit_note(self, *, name: str, vault_name: Optional[str]) -> NoteWithContentDTO:
        pass
