from models.fsdate import FSDate


class Partnership:
    def __init__(self, primary_id: str, secondary_id: str, partnership_type: str = "2", start_date: str | None = None, engagement_date: str | None = None, marriage_date: str | None = None, marriage_location: str | None = None, separation_date: str | None = None, divorce_date: str | None = None, annulment_date: str | None = None, end_date: str | None = None):
        '''
        Represents a partnership between two individuals.
        Partnership Basics:
        Tag	Fact	Example or Notes
        e 	(Ex-)partners	1 means the two people have been partners at some time.
        2 means the two people are current partners.
        Not needed if we know about the partnership for other reasons - see final notes.
        g 	Type of (ex-)partnership	m for married, e for engaged, r for generic relationship,
        s for separated, d for divorced, a for annulled,
        o for other + optional description e.g. oLife partnership
        Partnership Beginnings
        Tag	Fact	Example or Notes
        b 	Start date	YYYYMMDD - start of generic relationship (see above note on dates).
        r 	Engagement date	YYYYMMDD - see above note on dates.
        m 	Marriage date	YYYYMMDD - for all marriage-related partnerships, where g is m, s, d or a (see above note on dates).
        w 	Marriage location	Example: Las Vegas
        Partnership Endings
        Tag	Fact	Example or Notes
        s 	Separation date	YYYYMMDD - see above note on dates.
        d 	Divorce date	YYYYMMDD - see above note on dates.
        a 	Annulment date	YYYYMMDD - see above note on dates.
        z 	End date	YYYYMMDD - generic end of relationship, where g is m, e or r (see above note on dates).

        Two people are considered as current partners if either: (a) they are both specified as the other's primary partner via the s tag in i lines, or (b) they are declared as current partners (e2) in a line beginning p.
        Two people are considered as ex-partners if they are not current partners and either: (a) they have children in common, or (b) they are declared as ex-partners (e1) in a line beginning p.
        '''
        self.partners: list[str] = [primary_id, secondary_id]
        self.partnership_type: str = partnership_type
        self.start_date: FSDate | None = self.__parse_date(start_date)
        self.engagement_date: FSDate | None = self.__parse_date(engagement_date)
        self.marriage_date: FSDate | None = self.__parse_date(marriage_date)
        self.marriage_location: str | None = marriage_location
        self.separation_date: FSDate | None = self.__parse_date(separation_date)
        self.divorce_date: FSDate | None = self.__parse_date(divorce_date)
        self.annulment_date: FSDate | None = self.__parse_date(annulment_date)
        self.end_date: FSDate | None = self.__parse_date(end_date)
        self.current: bool = True if partnership_type == '2' else False
        self.ex_partners: bool = True if partnership_type == '1' else False


    def __parse_date(self, date: str | None) -> FSDate | None:
        try:
            return FSDate(date)
        except Exception as e:
            return None



