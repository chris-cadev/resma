import os
from resma.annotate.infrastructure.terminal_gateway import SystemCommandGateway
from resma.annotate.interfaces.interactors import AnnotateNoteEditorGateway


class CmdNoteEditorGateway(AnnotateNoteEditorGateway):
    def __init__(self, *, editor_cmd: str):
        super().__init__()
        self.editor_cmd = editor_cmd

    def open_editor(self, *, filepath):
        abs_filepath = os.path.realpath(filepath)
        SystemCommandGateway.run(f'{self.editor_cmd} "{abs_filepath}"')
