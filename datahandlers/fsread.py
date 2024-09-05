from models.fsdate import FSDate
from models.individual import Individual
from models.partnership import Partnership

class FSReader:
    def __init__self(self, path: str) -> None:
        '''
        - Can assume the path has been validated before being passed to the constructor.
        '''
        self.path: str = path
        self.individuals: list[Individual] = []
        self.partnerships: list[Partnership] = []
        self.__read_file()
    

    def __read_file(self) -> None:
        with open(self.path, 'r') as file:
            lines = file.readlines()