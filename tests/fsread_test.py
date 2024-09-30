from datahandlers.fsread import FSReader

def test_fsread():
    path = r'C:\Programming\GitHub\FamilyScript-py\Test_File_Parse-4-Sep-2024-203020485.txt'
    fsread = FSReader(path)
    for individual in fsread.individuals:
        print(individual)

    for partnership in fsread.partnerships:
        print(partnership)