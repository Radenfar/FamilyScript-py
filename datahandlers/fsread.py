from models.fsdate import FSDate
from models.individual import Individual
from models.partnership import Partnership

class FSReader:
    def __init__(self, path: str) -> None:
        '''
        - Can assume the path has been validated before being passed to the constructor.
        '''
        self.comments: list[str] = []
        self.path: str = path
        self.individuals: list[Individual] = []
        self.partnerships: list[Partnership] = []
        self.__read_file()
    

    def __read_file(self) -> None:
        with open(self.path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith('#'):
                self.comments.append((i, line))
            else:
                if line.startswith('i'):
                    self.individuals.append(self.__read_individual(line))
                elif line.startswith('p'):
                    self.partnerships.append(self.__read_partnership(line))
    

    def __read_individual(self, line: str) -> Individual:
        '''
        - Read individual information from lines[i] and return an Individual object.
        '''
        split_line = line.split()
        # ID is absolutely required, so we extract it first
        id = split_line.pop(0)[1:]
        new_individual = Individual(id, ["given_names_placeholder"])
        for info in split_line:
            detail = info[1:]
            if info.startswith('^'): # pointer
                new_individual.pointer = detail
            elif info.startswith('p'): # given names
                new_individual.given_names = detail.split(' ')
            elif info.startswith('N'): # nick name
                new_individual.nickname = detail
            elif info.startswith('T'): # title
                new_individual.title = detail
            elif info.startswith('J'): # suffix
                new_individual.suffix = detail
            elif info.startswith('l'): # surname now
                new_individual.surname_now = detail
            elif info.startswith('q'): # surname at birth
                new_individual.surname_at_birth = detail
            elif info.startswith('g'): # Gender
                # Gender is a special case. It is either: gm, gf or go + optional description
                if detail == 'm':
                    new_individual.gender = "Male"
                elif detail == 'f':
                    new_individual.gender = "Female"
                else:
                    new_individual.gender = detail[1:] # remove the 'o' and keep the description
            elif info.startswith('b'): # birth date
                new_individual.birth_date = detail
            elif info.startswith('z'): # deceased
                new_individual.deceased = detail
            elif info.startswith('d'): # death date
                new_individual.death_date = detail
            elif info.startswith('r'): # photo
                new_individual.photo = detail
            elif info.startswith('O'): # birth order
                new_individual.birth_order = detail
            elif info.startswith('m'): # mother
                new_individual.mother_id = detail
            elif info.startswith('f'): # father
                new_individual.father_id = detail
            elif info.startswith('V'): # primary parent set type
                new_individual.primary_parent_set_type = detail
            elif info.startswith('s'): # current partner
                new_individual.current_partner_id = detail
            elif info.startswith('X'): # mother (second parent set)
                new_individual.mother_second_id = detail
            elif info.startswith('Y'): # father (second parent set)
                new_individual.father_second_id = detail
            elif info.startswith('W'): # second parent set type
                new_individual.second_parent_set_type = detail
            elif info.startswith('K'): # mother (third parent set)
                new_individual.mother_third_id = detail
            elif info.startswith('L'): # father (third parent set)
                new_individual.father_third_id = detail
            elif info.startswith('Q'): # third parent set type
                new_individual.third_parent_set_type = detail
            elif info.startswith('e'): # email
                new_individual.email = detail
            elif info.startswith('w'): # website
                new_individual.website = detail
            elif info.startswith('B'): # blog
                new_individual.blog = detail
            elif info.startswith('P'): # photo site
                new_individual.photo_site = detail
            elif info.startswith('t'): # home tel
                new_individual.home_tel = detail
            elif info.startswith('k'): # work tel
                new_individual.work_tel = detail
            elif info.startswith('u'): # mobile
                new_individual.mobile = detail
            elif info.startswith('a'): # address
                new_individual.address = detail
            elif info.startswith('C'): # other contact
                new_individual.other_contact = detail
            elif info.startswith('v'): # birth place
                new_individual.birth_place = detail
            elif info.startswith('y'): # death place
                new_individual.death_place = detail
            elif info.startswith('Z'): # cause of death
                new_individual.cause_of_death = detail
            elif info.startswith('U'): # burial place
                new_individual.burial_place = detail
            elif info.startswith('F'): # burial date
                new_individual.burial_date = detail
            elif info.startswith('j'): # profession
                new_individual.profession = detail
            elif info.startswith('E'): # company
                new_individual.company = detail
            elif info.startswith('I'): # interests
                new_individual.interests = detail
            elif info.startswith('A'): # activities
                new_individual.activities = detail
            elif info.startswith('o'): # bio notes
                new_individual.bio_notes = detail
            else:
                print(f"Unknown tag: {info}")
        return new_individual


    def __read_partnership(self, line: str) -> Partnership:
        '''
        - Read partnership information from lines[i] and return a Partnership object.
        - The partnership information is in the lines following lines[i] until the next individual or partnership.
        '''
        split_line = line.split()
        print(split_line)
        return "partnership"