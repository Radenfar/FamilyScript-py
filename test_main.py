from tests.fsdate_test import test_fsdate

if __name__ == "__main__":
    print("""
    Correct output:
          - 6 May 31 BCE ~ 3 Mar 23 BCE
          - Approx 10 Oct 1
          - Before 17 Aug 17 BCE
          - After 1 Dec 1 BCE
          - 7 Nov 1
          - Approx 15 May 82
          - 4 Oct 2 ~ 6 Feb 6
          - After 15 Mar 88
    """)
    test_fsdate()
