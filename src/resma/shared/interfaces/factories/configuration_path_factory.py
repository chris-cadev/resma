import os
from os import getenv, makedirs
from os.path import dirname, join, expanduser, exists, abspath
import shutil


def make_config_path() -> str:
    is_dev_mode = getenv("RESMA_RUNTIME_MODE") == "dev"
    __self_dir__ = dirname(__file__)

    if is_dev_mode:
        config_dir = abspath(join(__self_dir__, "../../../../.."))
    elif os.name == "nt":
        appdata = getenv("APPDATA") or getenv("LOCALAPPDATA") or (
            join(expanduser("~"), ".config")
        )
        config_dir = join(appdata, "resma")
    else:
        config_dir = join(expanduser("~"), ".config", "resma")

    if not exists(config_dir):
        makedirs(config_dir, exist_ok=True)

    user_config_path = join(config_dir, "config.toml")
    if not exists(user_config_path):
        default_path = abspath(join(
            __self_dir__, "../../../default_config.toml"
        ))
        shutil.copy(default_path, user_config_path)

    return user_config_path
