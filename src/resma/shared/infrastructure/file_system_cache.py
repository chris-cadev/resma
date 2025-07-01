import json
from os import listdir, makedirs, remove
from os.path import abspath, dirname, exists, isfile, join
from typing import Optional

from resma.shared.infrastructure.interactors import CacheInteractor, JsonLike


class FileSystemCache(CacheInteractor):
    def __init__(self, *, cache_dir: str):
        self._cache_dir = abspath(cache_dir)

    def _get_filepath(self, key: str) -> str:
        return join(self._cache_dir, key)

    def get(self, *, key: str) -> Optional[str]:
        filepath = self._get_filepath(key)
        if not exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
                return json.loads(content)
            except json.JSONDecodeError:
                pass
        return None

    def set(self, *, key: str, value: JsonLike):
        filepath = self._get_filepath(key)
        makedirs(dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(value, f)

    def delete(self, *, key: str):
        filepath = self._get_filepath(key)
        if exists(filepath):
            remove(filepath)

    def clear(self):
        for filename in self.get_all_keys():
            self.delete(key=filename)

    def get_all_keys(self) -> list[str]:
        if not exists(self._cache_dir):
            return []
        return [
            f for f in listdir(self._cache_dir)
            if isfile(join(self._cache_dir, f))
        ]
