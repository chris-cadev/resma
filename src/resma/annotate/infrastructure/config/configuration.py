import toml
import os
from os.path import dirname, join, realpath
from typing import Any, Optional

from resma.annotate.interfaces.interactors import AnnotateConfigInteractor


class AnnotateConfiguration(AnnotateConfigInteractor):
    def __init__(self, *, path: Optional[str] = None):
        self.config_path = path

    def _get_working_directory(self, file: Optional[str] = None):
        """
        Returns the absolute directory of the given file,
        or the parent directory of this script if none is provided.
        """
        path = file if file else join(dirname(__file__), "..")
        return realpath(dirname(path))

    def get_config(self, path: Optional[str] = None, default: Optional[Any] = None):
        config = {}
        with open(self.config_path, 'r') as f:
            config = toml.load(f)
        if not path:
            return config
        return config.get(path, default)

    @property
    def vaults(self):
        return self.get_config('vaults', {})

    @property
    def default_note_name(self):
        return self.get_config('annotate', {}).get('default_note_name')

    @property
    def default_vault(self):
        return self.get_config('annotate', {}).get('default_vault')

    @property
    def editor_cmd(self):
        return str(self.get_config('editor_cmd', 'nano'))

    @property
    def workspace(self) -> str:
        path = self.get_config('workspace', '$HOME/.resma')

        if os.name == 'nt':
            path = path.replace('$HOME', '%USERPROFILE%')

        return str(os.path.expandvars(path))

    @property
    def templates_dir(self):
        config = self.get_config('templates', {}).get('config', {})
        directory = os.path.expanduser(config.get('dir', 'templates'))
        if os.path.isabs(directory):
            return directory
        return join(dirname(self.config_path), directory)

    @property
    def templates(self):
        config = self.get_config('templates', {})
        return {k: v for k, v in config.items() if k not in {"config"}}
