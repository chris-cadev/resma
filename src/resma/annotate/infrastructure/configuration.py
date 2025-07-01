import os
from os.path import dirname, join

from resma.annotate.interfaces.interactors import AnnotateConfigurationInteractor
from resma.shared.infrastructure.workspace_toml_configuration import WorkspacesTOMLConfiguration


class AnnotateConfiguration(AnnotateConfigurationInteractor, WorkspacesTOMLConfiguration):
    @property
    def vaults(self):
        return self.get_config('vaults', {})

    @property
    def default_note_name(self):
        global_config = self.get_config('default_note_name', None)
        annotate_config = (
            self.get_config(
                'annotate', {}).get(
                'default_note_name', None)
        )
        return annotate_config or global_config or 'untitled'

    @property
    def default_vault(self):
        global_config = self.get_config('default_vault', None)
        annotate_config = (
            self.get_config(
                'annotate', {}).get(
                'default_vault', None)
        )
        return annotate_config or global_config

    @property
    def editor_cmd(self):
        return str(self.get_config('editor_cmd', 'nano'))

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
