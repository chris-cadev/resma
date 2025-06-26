from resma.annotate.infrastructure.editor_gateway import CmdNoteEditorGateway
from resma.annotate.infrastructure.file_note_repository import FilesystemNoteRepository
from resma.annotate.interfaces.interactors import AnnotateConfigInteractor
from resma.annotate.use_cases.create_note.controllers import ClickCreateNoteController
from resma.annotate.use_cases.create_note.interactors import CreateNoteInteractor
from resma.annotate.use_cases.edit_note.controllers import ClickEditNoteController
from resma.annotate.use_cases.edit_note.interactors import EditNoteInteractor


def make_create_note_controller(config: AnnotateConfigInteractor) -> ClickCreateNoteController:
    return ClickCreateNoteController(
        create_note_interactor=CreateNoteInteractor(
            repository=FilesystemNoteRepository(),
            config=config
        )
    )


def make_edit_note_controller(env: AnnotateConfigInteractor) -> ClickEditNoteController:
    return ClickEditNoteController(
        edit_note_interactor=EditNoteInteractor(
            repository=FilesystemNoteRepository(),
            config=env,
            gateway=CmdNoteEditorGateway(editor_cmd=env.editor_cmd),
        )
    )
