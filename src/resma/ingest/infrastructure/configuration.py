import os
from os.path import join, dirname
from resma.ingest.interfaces.interactors import IngestConfigurationInteractor
from resma.shared.infrastructure.workspace_toml_configuration import WorkspacesTOMLConfiguration


class IngestConfiguration(IngestConfigurationInteractor, WorkspacesTOMLConfiguration):
    @property
    def default_vault(self):
        global_config = self.get_config('default_vault', None)
        ingest_config = (
            self.get_config(
                'ingest', {}).get(
                'default_vault', None)
        )
        return ingest_config or global_config

    @property
    def references_directory(self) -> str:
        return self.get_config('ingest', {}).get('references_directory', None)

    @property
    def media_directory(self) -> str:
        return self.get_config('ingest', {}).get('media_directory', None)

    @property
    def vaults(self):
        return self.get_config('vaults', {})

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
