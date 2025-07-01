from resma.ingest.infrastructure.configuration import IngestConfiguration
from resma.shared.interfaces.factories.configuration_path_factory import make_config_path


def make_ingest_configuration():
    config_path = make_config_path()
    return IngestConfiguration(path=config_path)
