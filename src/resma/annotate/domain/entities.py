class Note:
    def __init__(self, filepath: str):
        self.filepath = filepath
    @staticmethod
    def create(filepath: str):
        return Note(filepath)

class Media:
    def __init__(self, filepath: str):
        self.filepath = filepath
    # @staticmethod
    # def create(name: str, directory: str, extension: str):
    #     return Media(f"{directory}/{name}.{extension}")