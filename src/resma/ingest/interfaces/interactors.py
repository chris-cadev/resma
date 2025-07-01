
from abc import ABC, abstractmethod
from typing import Optional
from resma.shared.interfaces.dto import FileDTO
from resma.shared.interfaces.interactors import ConfigurationInteractor


class IngestConfigurationInteractor(ConfigurationInteractor, ABC):
    @property
    @abstractmethod
    def references_directory(self) -> str:
        pass

    @property
    @abstractmethod
    def media_directory(self) -> str:
        pass

    @property
    @abstractmethod
    def default_vault(self) -> str:
        pass

    @property
    @abstractmethod
    def vaults(self) -> dict:
        pass

    @property
    @abstractmethod
    def templates_dir(self) -> str:
        pass

    @property
    @abstractmethod
    def templates(self) -> str:
        pass


class IngestInteractor(ABC):
    @abstractmethod
    def create_reference(self, *, url: str, vault: Optional[str]) -> FileDTO:
        pass

    @abstractmethod
    def create_media_file(self, *, url: str, vault: Optional[str]) -> FileDTO:
        pass
