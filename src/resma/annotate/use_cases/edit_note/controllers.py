
import click
from resma.annotate.interfaces.dto import NoteWithContentDTO
from resma.annotate.interfaces.interactors import EditNoteController
from resma.shared.use_cases import Interactor


class ClickEditNoteController(EditNoteController):
    def __init__(self,*, edit_note_interactor: Interactor):
        self.edit_note_interactor = edit_note_interactor

    def edit_note(self, *, name, vault) -> NoteWithContentDTO:
        try:
            return self.edit_note_interactor.execute(
                name=name,
                vault=vault,
            )
        except ValueError as e:
            raise click.FileError(f'{vault}/{name}', e.args[0])