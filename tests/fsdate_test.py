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
    after = None
    for case in cases:
        print(f"CASE: {case}")
        fsdate = FSDate(case)
        print(f"OUTPUT: {fsdate}")
        after = fsdate.to_familyscript()
        print(f"OUTPUT: {after}")
        print(f"SUCCESS: {case == after}")