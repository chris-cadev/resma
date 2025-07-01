
from abc import ABC, abstractmethod
from typing import Any, Optional, Union
from furl import furl


class NoteEditorGateway(ABC):
    @abstractmethod
    def open(self, *, filepath: str) -> bool:
        pass


class InternetGateway(ABC):
    @abstractmethod
    def get_domain(self, *, url: str) -> str:
        pass

    @abstractmethod
    def get_mimetype(self, *, url: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_content(self, *, url: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_metadata(self, *, url: str) -> Optional[dict]:
        pass

JsonLike = Union[dict, list, tuple, str, int, float, bool]

class CacheInteractor(ABC):
    @abstractmethod
    def get(self, *, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, *, key: str, value: JsonLike) -> None:
        pass

    @abstractmethod
    def delete(self, *, key: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def get_all_keys(self) -> list[str]:
        pass


class InternetFetcherGateway(InternetGateway):
    def __init__(self, *, cache_interactor: CacheInteractor):
        super().__init__()
        self.cache = cache_interactor

    def get_domain(self, *, url):
        return furl(url).host

    def get_content(self, *, url):
        return self._fetch(url).get('html', None)

    def get_mimetype(self, *, url):
        return self._fetch(url).get('mimetype', None)

    def get_metadata(self, *, url):
        return self._fetch(url).get('metadata', None)

    @abstractmethod
    def _fetch(self, url: str) -> dict:
        pass
