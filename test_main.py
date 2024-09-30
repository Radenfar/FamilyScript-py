from FamilyScript import FamilyScript

if __name__ == '__main__':
      path = r'C:\Programming\GitHub\FamilyScript-py\Natasha-Taylor-30-Sep-2024-010901818.txt'
      fs = FamilyScript(path)
      # for individual in fs.individuals:
      #       try:
      #             print(individual)
      #       except UnicodeEncodeError as e:
      #             print(f"id: {individual.id} ERROR: {e}")
            # print(fs.get_children_with(individual, fs.individuals[0]))

      michael_martin = fs.get_by_name(given_names=['George'], surname='Martin')
      print(michael_martin)
      parents = fs.get_parents(michael_martin)
      print([parent.fullname for parent in parents])