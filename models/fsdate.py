from datetime import datetime
import re

class FSDate:
    def __init__(self, date: str | None = None) -> None:
        '''
        Custom handler for FamilyScript dates. These can be between two values or approximate. See the following documentation:
        Note on dates (tags b, d and F): Dates are specified in the Gregorian calendar in YYYYMMDD format. For example, July 14th 1968 is represented by 19680714. If only part of a date is known, the other parts can be padded with zeroes. For example, 19530000 means some time in 1953 and 00001106 means November 6th in an unknown year. Dates before the Common Era (BC/BCE) have a prefix B. For example, B00270330 means March 30th in the year 27 BCE. Symbol suffixes can be used to represent non-exact dates, where ~ means approximate, > means before the given date and < means after the given date. For example, 20050400~ means approximately April 2005. Date ranges are represented with a hyphen, e.g. 20030428-20040115 means between 28th April 2003 and 15th January 2004.
        link: https://www.familyecho.com/?page=familyscript
        '''
        self.primary_date: datetime | None = None
        self.secondary_date: datetime | None = None
        self.approximate: bool = False
        self.bce: bool = False
        self.before: bool = False
        self.after: bool = False
        self.__parse_date(date)
        self.familyscript: str = None
        if self.primary_date:
            self.familyscript = date


    @property
    def date(self) -> datetime | tuple[datetime, datetime] | None:
        if self.secondary_date:
            return self.primary_date, self.secondary_date
        return self.primary_date


    def __parse_date(self, date: str | None) -> None:
        if date is None:
            return
        if '-' in date:
            start_date, end_date = date.split('-')
            if 'B' in start_date and 'B' in end_date:
                # due to a bug in FamilyScript, if it's BCE then the ranges will be around the wrong way
                self.primary_date = self.__parse_single_date(end_date)
                self.secondary_date = self.__parse_single_date(start_date)
            else:
                self.primary_date = self.__parse_single_date(start_date)
                self.secondary_date = self.__parse_single_date(end_date)
        else:
            self.primary_date = self.__parse_single_date(date)


    def __parse_single_date(self, date: str) -> datetime | None:
        # Check for BCE prefix
        if date.startswith('B'):
            self.bce = True
            date = date[1:]

        # Check for approximate, before, after
        if date.endswith('~'):
            self.approximate = True
            date = date[:-1]
        elif date.endswith('>'):
            self.before = True
            date = date[:-1]
        elif date.endswith('<'):
            self.after = True
            date = date[:-1]

        # Extract year, month, and day with regex
        match = re.match(r'(\d{4})(\d{2})(\d{2})', date)
        if match:
            year, month, day = match.groups()
            year = int(year) if year != '0000' else None
            month = int(month) if month != '00' else None
            day = int(day) if day != '00' else None
            if year:
                return datetime(year=year, month=month or 1, day=day or 1)
        return None
    

    def custom_strf(self, _date: datetime) -> str:
        _date = _date.strftime("%d %b %Y")
        year = _date[-4:].replace("0", "")
        _date = _date[:-4] + year
        day = _date[:2]
        if day.startswith("0"):
            _date = _date[1:]
        return f"{_date} {"BCE" if self.bce else ""}"
    

    def to_familyscript(self) -> str:
        '''Deconverts the date back to FamilyScript format'''
        current_date: str = f"{self.primary_date.strftime('%Y%m%d')}"
        if self.bce:
            if self.secondary_date:
                return f"B{self.secondary_date.strftime('%Y%m%d')}-B{self.primary_date.strftime('%Y%m%d')}"
            else:
                current_date = f"B{current_date}"
        if self.approximate:
            current_date = f"{current_date}~"
        if self.before:
            current_date = f"{current_date}>"
        if self.after:
            current_date = f"{current_date}<"
        if self.secondary_date:
            return f"{current_date}-{self.secondary_date.strftime('%Y%m%d')}"
        return current_date
    

    def __str__(self) -> str:
        if self.approximate:
            return f"Approx {self.custom_strf(self.primary_date)}"
        if self.before:
            return f"Before {self.custom_strf(self.primary_date)}"
        if self.after:
            return f"After {self.custom_strf(self.primary_date)}"
        if self.secondary_date:
            return f"{self.custom_strf(self.primary_date)} ~ {self.custom_strf(self.secondary_date)}"
        return f"{self.custom_strf(self.primary_date)}"
    


