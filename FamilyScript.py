from datahandlers.fsread import FSReader
from datahandlers.fswrite import FSWriter
from models.fsdate import FSDate
from models.individual import Individual
from models.partnership import Partnership
import os
from collections import deque


class FamilyScript:
    def __init__(self, path: str) -> None:
        self.filepath = None
        if not self.__validate_path(path):
            raise FileNotFoundError(f"FamilyScript File not found: {path}")
        else:
            self.filepath = path
        self.reader: FSReader = FSReader(self.filepath)
        self.writer: FSWriter = FSWriter(self.filepath)
        self.individuals: list[Individual] = self.reader.get()[0]
        self.partnerships: list[Partnership] = self.reader.get()[1]
    

    @staticmethod
    def __validate_path(filepath: str) -> bool:
        return os.path.exists(filepath) and (filepath.endswith(".txt"))
    

    def get_members(self, partnership: Partnership | tuple[str, str]) -> tuple[Individual, Individual]:
        if isinstance(partnership, Partnership):
            for individual in self.individuals:
                if individual.id == partnership.partner1:
                    partner1 = individual
                if individual.id == partnership.partner2:
                    partner2 = individual
        else:
            for individual in self.individuals:
                if individual.id == partnership[0]:
                    partner1 = individual
                if individual.id == partnership[1]:
                    partner2 = individual
        return (partner1, partner2)
    

    def get_all_children(self, individual: Individual | str) -> list[Individual]:
        cur_id = individual.id if isinstance(individual, Individual) else individual
        children = []
        for potential_child in self.individuals:
            parent_ids = potential_child.get_all_parental_ids()
            if cur_id in parent_ids:
                children.append(potential_child)
        return children
    
    def get_individual(self, id: str) -> Individual:
        for individual in self.individuals:
            if individual.id == id:
                return individual
        return None

    def get_parents(self, individual: Individual | str, primary_only: bool = False) -> list[Individual]:
        cur_individual = individual if isinstance(individual, Individual) else self.get_individual(individual)
        if primary_only:
            return [self.get_individual(cur_individual.mother_id), self.get_individual(cur_individual.father_id)]
        all_parent_ids = cur_individual.get_all_parental_ids()
        return [self.get_individual(parent_id) for parent_id in all_parent_ids]
    

    def get_children_with(self, individual_1: Individual | str, individual_2: Individual | str) -> list[Individual]:
        cur_id_1 = individual_1.id if isinstance(individual_1, Individual) else individual_1
        cur_id_2 = individual_2.id if isinstance(individual_2, Individual) else individual_2
        if cur_id_1 == cur_id_2:
            return []
        children = []
        for potential_child in self.individuals:
            if cur_id_1 in [potential_child.father_id, potential_child.mother_id] and cur_id_2 in [potential_child.father_id, potential_child.mother_id]:
                children.append(potential_child)
        return children


    def find_siblings_by_parent(self, individual: Individual | str, parent_id: str) -> list[Individual]:
        cur_individual = individual if isinstance(individual, Individual) else self.get_individual(individual)
        return [sibling for sibling in self.individuals if parent_id in sibling.get_all_parental_ids() and sibling.id != cur_individual.id]


    def get_siblings(self, individual: Individual | str, include_half_siblings: bool = False) -> list[Individual] | list[list[Individual]]:
        '''
        - get_siblings(same_parents):
            > if include_half_siblings is False, returns a list of full siblings (same mother and father)
            > if include_half_siblings is True, returns [full_siblings, maternal_half_siblings, paternal_half_siblings]
        '''
        cur_individual = individual if isinstance(individual, Individual) else self.get_individual(individual)

        # Get full siblings (same mother and father)
        full_siblings = []
        for potential_full_sibling in self.individuals:
            if (cur_individual.id != potential_full_sibling.id and
                cur_individual.mother_id == potential_full_sibling.mother_id and
                cur_individual.mother_id != None and
                cur_individual.father_id == potential_full_sibling.father_id and
                cur_individual.father_id != None):
                full_siblings.append(potential_full_sibling)
        
        if not include_half_siblings:
            return full_siblings

        # Get half-siblings (either same mother or same father)
        maternal_half_siblings = []
        paternal_half_siblings = []
        for potential_half_sibling in self.individuals:
            if cur_individual.id != potential_half_sibling.id:
                # Maternal half-siblings (same mother, different father)
                if (cur_individual.mother_id == potential_half_sibling.mother_id and
                    cur_individual.mother_id != None and
                    cur_individual.father_id != potential_half_sibling.father_id and
                    cur_individual.father_id != None):
                    maternal_half_siblings.append(potential_half_sibling)

                # Paternal half-siblings (same father, different mother)
                elif (cur_individual.father_id == potential_half_sibling.father_id and
                    cur_individual.father_id != None and
                    cur_individual.mother_id != potential_half_sibling.mother_id and
                    cur_individual.mother_id != None):
                    paternal_half_siblings.append(potential_half_sibling)

        return [full_siblings, maternal_half_siblings, paternal_half_siblings]
    

    def get_by_name(self, given_names: list[str], surname: str, exact = True) -> Individual | list[Individual]:
        exacts = []
        if exact:
            for individual in self.individuals:
                if individual.given_names == given_names and (individual.surname_now == surname or individual.surname_at_birth == surname):
                    exacts.append(individual)
            return exacts
        else:
            potentials = []
            for individual in self.individuals:
                if individual.given_names == given_names and individual.surname_now == surname or individual.surname_at_birth == surname:
                    return individual
                elif individual.given_names == given_names:
                    potentials.append(individual)
            return potentials

    def calculate_distance(self, individual_1: Individual | str, individual_2: Individual | str) -> int:
        """
        Returns the 'distance' between two individuals in the family tree, where the distance 
        refers to the number of connections/steps between them. Full siblings are considered 
        to have no distance, meaning traversing full siblings adds 0 to the distance.
        
        Distance:
        - 0 for the same individual
        - 1 for parent-child or half-sibling connections
        - 2 for grandparent, grandchild, etc.
        - Special: Full siblings don't increase the distance (distance remains the same).

        """
        start_individual = individual_1 if isinstance(individual_1, Individual) else self.get_individual(individual_1)
        target_individual = individual_2 if isinstance(individual_2, Individual) else self.get_individual(individual_2)
        
        if start_individual == target_individual:
            return 0  # Same individual

        # Use BFS to find the shortest path
        visited = set()  # Track visited individuals
        queue = deque([(start_individual, 0)])  # (current individual, current distance)

        while queue:
            current_individual, current_distance = queue.popleft()

            # Mark the current individual as visited
            visited.add(current_individual.id)

            # Check if we've reached the target individual
            if current_individual == target_individual:
                return current_distance

            # Get parents, children, and siblings (full and half)
            parents = self.get_parents(current_individual)
            children = self.get_all_children(current_individual)
            siblings = self.get_siblings(current_individual, include_half_siblings=True)

            full_siblings, maternal_half_siblings, paternal_half_siblings = siblings if isinstance(siblings, list) else (siblings, [], [])

            # Traverse parents, children, and half-siblings (add +1 distance)
            for relative in parents + children + maternal_half_siblings + paternal_half_siblings:
                if relative and relative.id not in visited:
                    queue.append((relative, current_distance + 1))

            # Traverse full siblings (distance remains the same, so no +1)
            for sibling in full_siblings:
                if sibling.id not in visited:
                    queue.append((sibling, current_distance))  # Distance remains the same

        # If no connection is found, return a large number (infinite distance)
        return float('inf')