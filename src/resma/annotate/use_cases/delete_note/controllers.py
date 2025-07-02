
import click
from resma.shared.interfaces.dto import FileDTO
from resma.annotate.interfaces.interactors import DeleteNoteController
from resma.shared.use_cases import Interactor


class ClickDeleteNoteController(DeleteNoteController):
    def __init__(self,*, interactor: Interactor):
        self.interactor = interactor

    def delete_note(self, *, name, vault) -> FileDTO:
        try:
            return self.interactor.execute(
                name=name,
                vault=vault,
            )
        except ValueError as e:
            raise click.FileError(f'{vault}/{name}', e.args[0])