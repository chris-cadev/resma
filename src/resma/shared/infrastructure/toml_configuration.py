import toml
from typing import Any, Optional

from resma.shared.interfaces.interactors import ConfigurationInteractor


class TOMLConfiguration(ConfigurationInteractor):
    def __init__(self, *, path: Optional[str] = None):
        self.config_path = path

    def get_config(self, key: Optional[str] = None, default_value: Optional[Any] = None):
        config = {}
        with open(self.config_path, 'r') as f:
            config = toml.load(f)
        if not key:
            return config
        return config.get(key, default_value)