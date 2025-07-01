import os
from resma.annotate.interfaces.dto import TemplateDTO
from resma.annotate.interfaces.interactors import TemplateRepositoryInteractor


class FileTemplatesRepository(TemplateRepositoryInteractor):
    def get(self, *, filepath: str):
        if not os.path.exists(filepath):
            raise ValueError(f"Template {filepath} does not exist")
        with open(filepath) as n:
            return TemplateDTO(
                filepath=filepath,
                content=n.read()
            )
        raise SystemError('Unexpected error', {'filepath': filepath})
