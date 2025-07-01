from resma.annotate.infrastructure.configuration import AnnotateConfiguration
from resma.shared.interfaces.factories.configuration_path_factory import make_config_path


def make_annotate_configuration():
    config_path = make_config_path()
    return AnnotateConfiguration(path=config_path)
