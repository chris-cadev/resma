class File:
    def __init__(self, filepath: str):
        self.filepath = filepath


class Note(File):
    @staticmethod
    def create(*, filepath) -> 'Note':
        return Note(filepath=filepath)


class Template(File):
    @staticmethod
    def create(*, filepath) -> 'Template':
        return Template(filepath=filepath)


class Media(File):
    ...
