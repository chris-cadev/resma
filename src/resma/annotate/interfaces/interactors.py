from abc import ABC, abstractmethod
from typing import Optional, Union

from resma.annotate.domain.entities import Note
from resma.annotate.interfaces.dto import CreateNoteDTO


class AnnotateEnvInteractor(ABC):
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


class AnnotateNoteRepositoryInteractor(ABC):
    @abstractmethod
    def create(self, *, note: Note, content: Union[str, None]) -> Union[Note, Exception]:
        pass

    # @abstractmethod
    # def get(self, *, note_filepath: str) -> Union[Note, None, Exception]:
    #     pass

    # @abstractmethod
    # def list(self, *, vault_name: Optional[str] = None) -> Union[list[Note], None, Exception]:
    #     pass

    # @abstractmethod
    # def delete(self, *, note_filepath: str) -> Union[bool, Exception]:
    #     pass


class CreateNoteController(ABC):
    @abstractmethod
    def create_note(self, *, name: str, vault_name: Optional[str], template: Optional[str] = None) -> CreateNoteDTO:
        pass
