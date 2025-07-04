
import click
from resma.shared.interfaces.dto import TextFileWithContentDTO
from resma.annotate.interfaces.interactors import EditNoteController
from resma.shared.use_cases import Interactor


class ClickEditNoteController(EditNoteController):
    def __init__(self, *, interactor: Interactor):
        self.interactor = interactor

    def edit_note(self, *, name, vault) -> TextFileWithContentDTO:
        try:
            return self.interactor.execute(
                name=name,
                vault=vault,
            )
        except ValueError as e:
            raise click.FileError(f'{vault}/{name}', e.args[0])