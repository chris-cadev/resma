
from abc import ABC, abstractmethod
from typing import Any, Optional


class ConfigurationInteractor(ABC):
    @abstractmethod
    def get_config(self, key: Optional[str] = None, default_value: Optional[Any] = None) -> Any:
        pass


class WorkspaceConfigurationInteractor(ConfigurationInteractor, ABC):
    @property
    @abstractmethod
    def workspace(self) -> str:
        pass