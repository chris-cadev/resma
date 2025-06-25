
from resma.annotate.interfaces.interactors import CreateNoteController
from resma.annotate.use_cases.create_note.interactor import CreateNoteInteractor
from resma.shared.use_cases import Interactor


class ClickCreateUserController(CreateNoteController):
    def __init__(self,*, create_note_interactor: Interactor):
        self.create_note_interactor = create_note_interactor

    def create_note(self, *, name, vault_name, template=None):
        return self.create_note_interactor.execute(
            name=name,
            vault=vault_name,
            template=template
        )
