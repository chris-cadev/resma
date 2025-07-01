import os

from resma.shared.infrastructure.toml_configuration import TOMLConfiguration
from resma.shared.interfaces.interactors import WorkspaceConfigurationInteractor

class WorkspacesTOMLConfiguration(WorkspaceConfigurationInteractor, TOMLConfiguration):
    @property
    def workspace(self) -> str:
        path = self.get_config('workspace', '$HOME/.resma')

        if os.name == 'nt':
            path = path.replace('$HOME', '%USERPROFILE%')

        return str(os.path.expandvars(path))