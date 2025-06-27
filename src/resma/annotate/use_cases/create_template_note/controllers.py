
from typing import Optional

import click
from resma.annotate.interfaces.dto import NoteDTO
from resma.annotate.interfaces.interactors import CreateTemplateNoteController
from resma.shared.use_cases import Interactor


class ClickCreateTemplateNoteController(CreateTemplateNoteController):
    def __init__(self,*, interactor: Interactor):
        self.interactor = interactor

    def create_note(self, *, name: Optional[str], vault: Optional[str], template: Optional[str]=None, meta: dict) -> NoteDTO:
        try:
            return self.interactor.execute(
                name=name,
                vault=vault,
                template=template,
                meta=meta,
            )
        except ValueError as e:
            click.echo(f"Error creating note: {e}")
