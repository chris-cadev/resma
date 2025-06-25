from resma.annotate.infrastructure.note_repository import FilesystemNoteRepository
from resma.annotate.interfaces.factories.environment_factory import make_annotate_environment
from resma.annotate.interfaces.interactors import AnnotateEnvInteractor
from resma.annotate.use_cases.create_note.controller import ClickCreateUserController
from resma.annotate.use_cases.create_note.interactor import CreateNoteInteractor


def make_create_note_controller(env: AnnotateEnvInteractor) -> ClickCreateUserController:
    return ClickCreateUserController(
        create_note_interactor=CreateNoteInteractor(
            repository=FilesystemNoteRepository(),
            env=env
        )
    )