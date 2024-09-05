from models.fsdate import FSDate

class Individual:
    def __init__(self, id: str, given_names: list[str], nickname: str | None = None, title: str | None = None, surname_now: str | None = None, surname: str | None = None, surname_at_birth: str | None = None, gender: str | None = None, birth_date: str | None = None, deceased: str | None = None, death_date: str | None = None, photo: str | None = None, birth_order: str | None = None, mother: str | None = None, father: str | None = None, primary_parent_set_type: str | None = None, current_partner: str | None = None, mother_second: str | None = None, father_second: str | None = None, second_parent_set_type: str | None = None, mother_third: str | None = None, father_third: str | None = None, third_parent_set_type: str | None = None, email: str | None = None, website: str | None = None, blog: str | None = None, photo_site: str | None = None, home_tel: str | None = None, work_tel: str | None = None, mobile: str | None = None, address: str | None = None, other_contact: str | None = None, birth_place: str | None = None, death_place: str | None = None, cause_of_death: str | None = None, burial_place: str | None = None, burial_date: str | None = None, profession: str | None = None, company: str | None = None, interests: str | None = None, activities: str | None = None, bio_notes: str | None = None) -> None:
        '''
        Personal Information
        Tag	Fact	Example or Notes
        p 	Given names	Separated by spaces, e.g. Mary Alice
        N 	Nickname	Example: Peanut
        T 	Title	Example: Dr
        J 	Suffix	Example: III
        l 	Surname now	Example: Smith
        q 	Surname at birth	Example: Jones
        g 	Gender	m for male, f for female, o for other + optional description e.g. oTrans
        b 	Birth date	YYYYMMDD - see note on dates.
        z 	Deceased	1 to indicate that person has died.
        d 	Death date	YYYYMMDD - see note on dates.
        r 	Photo	imageid width height - see note on images.
        O 	Birth order	See note on birth order.
        Relationships
        Tag	Fact	Example or Notes
        m 	Mother (primary parent set)	ID of mother, e.g. F4XB6
        f 	Father (primary parent set)	ID of father, e.g. JD80F
        V 	Primary parent set type	b for biological, a for adopted, f for foster, s for step, g for god
        s 	Current partner	ID of current partner, e.g. PWAN7
        X 	Mother (second parent set)	ID of mother in second parent set, e.g. K1NY5
        Y 	Father (second parent set)	ID of father in second parent set, e.g. JD80F
        W 	Second parent set type	b for biological, a for adopted, f for foster, s for step, g for god
        K 	Mother (third parent set)	ID of mother in third parent set, e.g. S79ZW
        L 	Father (third parent set)	ID of father in third parent set, e.g. L4P3V
        Q 	Third parent set type	b for biological, a for adopted, f for foster, s for step, g for god
        Contact Information
        Tag	Fact	Example or Notes
        e 	Email	Example: mary@smith.org
        w 	Website	Example: http://www.mary.com/
        B 	Blog	Example: http://mary.blogspot.com/
        P 	Photo site	Example: http://www.mary.com/photos/
        t 	Home tel	Example: 212 123 4567
        k 	Work tel	Example: 212 789 3456
        u 	Mobile	Example: 212 123 2468
        a 	Address	Example: 123 Mass Ave\nNew York 10024\nUSA
        C 	Other contact	Example: ICQ maryalice123
        Biographical Information
        Tag	Fact	Example or Notes
        v 	Birth place	Example: Chicago
        y 	Death place	Ignored if person has not died (see z)
        Z 	Cause of death	Ignored if person has not died (see z)
        U 	Burial place	Ignored if person has not died (see z)
        F 	Burial date	YYYYMMDD - see note on dates.
        j 	Profession	Example: Administrator
        E 	Company	Example: Acme Corporation
        I 	Interests	Example: Movies, literature, history
        A 	Activities	Example: Travel, painting
        o 	Bio notes	Example: Also lived in Netherlands
        
        The only required fields are ID and given names, all other fields are optional.
        '''
        self.id: str = id
        self.given_names: list[str] = given_names
        self.nickname: str | None = nickname
        self.title: str | None = title
        self.surname_now: str | None = surname_now
        self.surname_at_birth: str | None = surname_at_birth
        self.gender: str | None = gender
        self.birth_date: FSDate | None = self.__parse_date(birth_date)
        self.deceased: bool = True if deceased == "1" else False
        self.death_date: FSDate | None = self.__parse_date(death_date) if deceased == "1" else None
        self.photo: str | None = photo
        self.birth_order: str | None = birth_order
        self.mother_id: str | None = mother
        self.father_id: str | None = father
        self.primary_parent_set_type: str | None = primary_parent_set_type
        self.current_partner_id: str | None = current_partner
        self.mother_second_id: str | None = mother_second
        self.father_second_id: str | None = father_second
        self.second_parent_set_type: str | None = second_parent_set_type
        self.mother_third_id: str | None = mother_third
        self.father_third_id: str | None = father_third
        self.third_parent_set_type: str | None = third_parent_set_type
        self.email: str | None = email
        self.website: str | None = website
        self.blog: str | None = blog
        self.photo_site: str | None = photo_site
        self.home_tel: str | None = home_tel
        self.work_tel: str | None = work_tel
        self.mobile: str | None = mobile
        self.address: str | None = address
        self.other_contact: str | None = other_contact
        self.birth_place: str | None = birth_place
        self.death_place: str | None = death_place if deceased == "1" else None
        self.cause_of_death: str | None = cause_of_death if deceased == "1" else None
        self.burial_place: str | None = burial_place if deceased == "1" else None
        self.burial_date: FSDate | None = self.__parse_date(burial_date) if deceased == "1" else None
        self.profession: str | None = profession
        self.company: str | None = company
        self.interests: str | None = interests
        self.activities: str | None = activities
        self.bio_notes: str | None = bio_notes


    def __parse_date(self, date: str | None) -> FSDate | None:
        try:
            return FSDate(date)
        except Exception as e:
            return None