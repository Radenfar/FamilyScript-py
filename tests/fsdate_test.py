from models.fsdate import FSDate



def test_fsdate():
    cases: list[str] = [
        "B00230303-B00310506",
        "00011010~",
        "B00170817>",
        "B00011201<",
        "00011107",
        "00820515~",
        "00021004-00060206",
        "00880315"
    ]
    for case in cases:
        fsdate = FSDate(case)
        print(fsdate)