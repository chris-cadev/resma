from resma.annotate.use_cases.delete_note.controllers import ClickDeleteNoteController
from resma.annotate.use_cases.delete_note.interactors import DeleteNoteInteractor
from resma.shared.infrastructure.editor_gateway import SystemCommandNoteEditorGateway
from resma.annotate.infrastructure.note_file_repository import NoteFilesRepository
from resma.shared.infrastructure.template_file_repository import FileTemplatesRepository
from resma.annotate.interfaces.interactors import AnnotateConfigurationInteractor
from resma.annotate.use_cases.create_note.controllers import ClickCreateNoteController
from resma.annotate.use_cases.create_note.interactors import CreateNoteInteractor
from resma.annotate.use_cases.create_template_note.controllers import ClickCreateTemplateNoteController
from resma.annotate.use_cases.create_template_note.interactors import CreateTemplateNoteInteractor, TimelineNoteInteractor
from resma.annotate.use_cases.edit_note.controllers import ClickEditNoteController
from resma.annotate.use_cases.edit_note.interactors import EditNoteInteractor


def make_create_note_controller(config: AnnotateConfigurationInteractor):
    return ClickCreateNoteController(
        create_note_interactor=CreateNoteInteractor(
            notes_repo=NoteFilesRepository(),
            config=config
        )
    )


def make_create_template_note_controller(config: AnnotateConfigurationInteractor):
    return ClickCreateTemplateNoteController(
        interactor=CreateTemplateNoteInteractor(
            notes_repo=NoteFilesRepository(),
            config=config,
            templates_repo=FileTemplatesRepository(),
            note_template_interactor=TimelineNoteInteractor(),
        )
    )


def make_edit_note_controller(env: AnnotateConfigurationInteractor) -> ClickEditNoteController:
    return ClickEditNoteController(
        interactor=EditNoteInteractor(
            repository=NoteFilesRepository(),
            config=env,
            editor=SystemCommandNoteEditorGateway(editor_cmd=env.editor_cmd),
        )
    )


def make_delete_note_controller(configuration: AnnotateConfigurationInteractor) -> ClickEditNoteController:
    return ClickDeleteNoteController(
        interactor=DeleteNoteInteractor(
            notes_repo=NoteFilesRepository(),
            config=configuration,
        )
    )
