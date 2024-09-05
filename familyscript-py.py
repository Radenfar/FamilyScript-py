import os


class FamilyScript:
    def __init__(self, filepath: str) -> None:
        if not self.__validate_path(filepath):
            raise FileNotFoundError(f"FamilyScript File not found: {filepath}")
        self.filepath = filepath
        


    @staticmethod
    def __validate_path(filepath: str) -> bool:
        return os.path.exists(filepath) and (filepath.endswith(".txt"))