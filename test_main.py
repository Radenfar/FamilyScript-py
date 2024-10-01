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

      kathleen_mary_raine = fs.get_by_name(given_names=['Kathleen', 'Mary'], surname='Raine')[0]
      print(kathleen_mary_raine.fullname)

      percy_jackson_p_raine = fs.get_by_name(given_names=['Percy', 'Jackson', 'P'], surname='Raine')[0]
      print(percy_jackson_p_raine.fullname)

      print(fs.calculate_distance(kathleen_mary_raine, percy_jackson_p_raine))