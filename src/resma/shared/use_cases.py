from abc import ABC, abstractmethod
from typing import Any


class Interactor(ABC):
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Child classes must implement this method, with their own parameters."""
        pass