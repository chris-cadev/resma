import toml
import os
from typing import Optional

from resma.annotate.interfaces.interactors import AnnotateConfigInteractor


class AnnotateConfiguration(AnnotateConfigInteractor):
    def __init__(self, *, path: Optional[str] = None):
        self.config_path = path

    def _get_working_directory(self, file: Optional[str] = None):
        """
        Returns the absolute directory of the given file,
        or the parent directory of this script if none is provided.
        """
        path = file if file else os.path.join(os.path.dirname(__file__), "..")
        return os.path.realpath(os.path.dirname(path))

    def get_config(self) -> dict:
        config = {}
        with open(self.config_path, 'r') as f:
            config = toml.load(f)
        return config

    @property
    def vaults(self):
        return self.get_config().get('vaults', {})

    @property
    def default_note_name(self):
        return self.get_config().get('annotate', {}).get('default_note_name')

    @property
    def default_vault(self):
        return self.get_config().get('annotate', {}).get('default_vault')

    @property
    def editor_cmd(self):
        return self.get_config().get('editor_cmd', 'nano')

    @property
    def workspace(self) -> str:
        path = self.get_config().get('workspace', '$HOME/.resma')

        if os.name == 'nt':
            path = path.replace('$HOME', '%USERPROFILE%')

        return os.path.expandvars(path)
