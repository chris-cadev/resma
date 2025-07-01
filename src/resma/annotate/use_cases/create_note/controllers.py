
from resma.shared.interfaces.dto import FileDTO
from resma.annotate.interfaces.interactors import CreateNoteController
from resma.shared.use_cases import Interactor


class ClickCreateNoteController(CreateNoteController):
    def __init__(self,*, create_note_interactor: Interactor):
        self.create_note_interactor = create_note_interactor

    def create_note(self, *, name, vault) -> FileDTO:
        return self.create_note_interactor.execute(
            name=name,
            vault=vault,
        )
