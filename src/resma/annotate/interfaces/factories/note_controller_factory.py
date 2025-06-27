from resma.annotate.infrastructure.editor_gateway import CmdNoteEditorGateway
from resma.annotate.infrastructure.note_file_repository import NoteFilesRepository
from resma.annotate.infrastructure.template_file_repository import TemplateFilesRepository
from resma.annotate.interfaces.interactors import AnnotateConfigInteractor
from resma.annotate.use_cases.create_note.controllers import ClickCreateNoteController
from resma.annotate.use_cases.create_note.interactors import CreateNoteInteractor
from resma.annotate.use_cases.create_template_note.controllers import ClickCreateTemplateNoteController
from resma.annotate.use_cases.create_template_note.interactors import CreateTemplateNoteInteractor, TimelineNoteInteractor
from resma.annotate.use_cases.edit_note.controllers import ClickEditNoteController
from resma.annotate.use_cases.edit_note.interactors import EditNoteInteractor


def make_create_note_controller(config: AnnotateConfigInteractor):
    return ClickCreateNoteController(
        create_note_interactor=CreateNoteInteractor(
            notes_repo=NoteFilesRepository(),
            config=config
        )
    )


def make_create_template_note_controller(config: AnnotateConfigInteractor):
    return ClickCreateTemplateNoteController(
        interactor=CreateTemplateNoteInteractor(
            notes_repo=NoteFilesRepository(),
            config=config,
            templates_repo=TemplateFilesRepository(),
            note_template_interactor=TimelineNoteInteractor(),
        )
    )


def make_edit_note_controller(env: AnnotateConfigInteractor) -> ClickEditNoteController:
    return ClickEditNoteController(
        edit_note_interactor=EditNoteInteractor(
            repository=NoteFilesRepository(),
            config=env,
            gateway=CmdNoteEditorGateway(editor_cmd=env.editor_cmd),
        )
    )
