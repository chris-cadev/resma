import os
from resma.shared.infrastructure.terminal_gateway import SystemCommandGateway
from resma.shared.infrastructure.interactors import NoteEditorGateway


class SystemCommandNoteEditorGateway(NoteEditorGateway):
    def __init__(self, *, editor_cmd: str):
        super().__init__()
        self.editor_cmd = editor_cmd

    def open(self, *, filepath):
        abs_filepath = os.path.realpath(filepath)
        SystemCommandGateway.run(f'{self.editor_cmd} "{abs_filepath}"')
