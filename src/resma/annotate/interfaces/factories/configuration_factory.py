from os import getenv, makedirs
from os.path import join, expanduser, exists, dirname, abspath
import shutil
from typing import Optional

from resma.annotate.infrastructure.config.configuration import AnnotateConfiguration


def get_config_path() -> Optional[str]:
    is_dev_mode = getenv("RESMA_RUNTIME_MODE") == "dev"

    if is_dev_mode:
        return abspath(join(dirname(__file__), "../../../../../config.toml"))

    user_config_dir = join(expanduser("~"), ".config", "resma")
    user_config_path = join(user_config_dir, "config.toml")

    if exists(user_config_path):
        return user_config_path

    makedirs(user_config_dir, exist_ok=True)

    default_path = abspath(
        join(dirname(__file__), "../../../default_config.toml"))
    shutil.copy(default_path, user_config_path)

    return user_config_path


def make_annotate_configuration():
    config_path = get_config_path()
    return AnnotateConfiguration(path=config_path)
