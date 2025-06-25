import toml
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from resma.annotate.interfaces.interactors import AnnotateEnvInteractor


class AnnotateEnvironment(AnnotateEnvInteractor):
    def __init__(self):
        self._workspace = None
        self._init_env()

    def get_working_directory(self, file: Optional[str] = None):
        """
        Returns the absolute directory of the given file,
        or the parent directory of this script if none is provided.
        """
        path = file if file else os.path.join(os.path.dirname(__file__), "..")
        return os.path.realpath(os.path.dirname(path))

    def get_config(self) -> dict:
        config_path = os.path.join(
            self.get_working_directory(), "../../../config.toml")
        config = {}
        with open(config_path, 'r') as f:
            config = toml.load(f)
        return config

    def load_env(self):
        CWD = self.get_working_directory()
        ENV_FILE_PATH = Path(os.path.join(CWD, ".env"))
        load_dotenv(dotenv_path=ENV_FILE_PATH)

    def _init_env(self):
        self.load_env()

        self.annotate_untitled_name = os.getenv(
            "ANNOTATE_UNTITLED_NAME", "untitled")
        self.annotate_default_vault = os.getenv("ANNOTATE_DEFAULT_VAULT")
        self.annotate_vaults = self.get_config()["vaults"]

    @property
    def workspace(self):
        if self._workspace is None:
            workspace = os.getenv("WORKSPACE", "$HOME")
            if os.name == "nt":
                workspace = workspace.replace("$HOME", "%USERPROFILE%")
            self._workspace = os.path.expandvars(workspace)
        return self._workspace

    @property
    def vaults(self):
        return self.annotate_vaults

    @property
    def default_note_name(self):
        return self.annotate_default_vault

    @property
    def default_vault(self):
        return self.annotate_default_vault
