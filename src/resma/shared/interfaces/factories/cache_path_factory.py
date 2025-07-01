import os
from os import getenv, makedirs
from os.path import dirname, join, expanduser, exists, abspath


def make_cache_path() -> str:
    is_dev_mode = getenv("RESMA_RUNTIME_MODE") == "dev"
    __dir__ = dirname(__file__)

    if is_dev_mode:
        cache_dir = abspath(join(__dir__, "../../../../../.cache"))
    elif os.name == 'nt':
        appdata = getenv("LOCALAPPDATA") or getenv("APPDATA") or join(expanduser("~"), ".cache")
        cache_dir = abspath(join(appdata, "resma"))
    else:
        cache_dir = abspath(join(expanduser("~"), ".cache", "resma"))

    if not exists(cache_dir):
        makedirs(cache_dir, exist_ok=True)

    return cache_dir
