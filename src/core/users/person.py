import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

class PersonGender(str, Enum):
    MALE = "M"
    FEMALE = "F"

class BloodType(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class MaritalStatus(str, Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"
    SEPARATED = "SEPARATED"
    DOMESTIC_PARTNERSHIP = "DOMESTIC_PARTNERSHIP"

class EducationLevel(str, Enum):
    NO_EDUCATION = "NO_EDUCATION"
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    HIGH_SCHOOL = "HIGH_SCHOOL"
    ASSOCIATES = "ASSOCIATES"
    BACHELORS = "BACHELORS"
    MASTERS = "MASTERS"
    DOCTORATE = "DOCTORATE"
    POST_DOCTORATE = "POST_DOCTORATE"

class EmploymentStatus(str, Enum):
    EMPLOYED = "EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    STUDENT = "STUDENT"
    RETIRED = "RETIRED"
    HOMEMAKER = "HOMEMAKER"

class RelationshipType(str, Enum):
    PARENT = "PARENT"
    CHILD = "CHILD"
    SIBLING = "SIBLING"
    SPOUSE = "SPOUSE"
    FRIEND = "FRIEND"
    COLLEAGUE = "COLLEAGUE"
    ACQUAINTANCE = "ACQUAINTANCE"
    OTHER = "OTHER"

@dataclass
class PersonBody:
    gender: PersonGender
    """
    The user gender can be M or F its of type 'PersonGender'
    """
    age: 15
    """
    The user age
    """
    height: int
    """
    The use height in centimeters
    """
    weight: int
    """
    The user Weight in kilos
    """

@dataclass
class PersonCitizenship:
    birth: datetime
    """
    THe user birthdate as a datetime obj
    """
    name: str
    """
    The user full name
    """
    nationality: str
    """
    The user nationality
    """

@dataclass
class ContactInfo:
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = ""
    emergency_contact_name: str = ""
    emergency_contact_phone: str = ""

@dataclass
class MedicalInfo:
    blood_type: Optional[BloodType] = None
    allergies: List[str] = None
    medications: List[str] = None
    medical_conditions: List[str] = None
    insurance_provider: str = ""
    insurance_policy_number: str = ""
    last_physical_exam: Optional[datetime] = None
    vaccination_history: Dict[str, datetime] = None

    def __post_init__(self):
        if self.allergies is None:
            self.allergies = []
        if self.medications is None:
            self.medications = []
        if self.medical_conditions is None:
            self.medical_conditions = []
        if self.vaccination_history is None:
            self.vaccination_history = {}

@dataclass
class EmploymentInfo:
    status: EmploymentStatus = EmploymentStatus.UNEMPLOYED
    current_employer: str = ""
    job_title: str = ""
    start_date: Optional[datetime] = None
    salary: float = 0.0
    work_history: List[Dict[str, Union[str, datetime, float]]] = None

    def __post_init__(self):
        if self.work_history is None:
            self.work_history = []

@dataclass
class Relationship:
    person_id: str
    relationship_type: RelationshipType
    start_date: Optional[datetime] = None
    notes: str = ""

@dataclass
class SocialInfo:
    marital_status: MaritalStatus = MaritalStatus.SINGLE
    relationships: List[Relationship] = None
    social_media_accounts: Dict[str, str] = None

    def __post_init__(self):
        if self.relationships is None:
            self.relationships = []
        if self.social_media_accounts is None:
            self.social_media_accounts = {}

@dataclass
class PersonPreferences:
    dietary: List[str] = None
    hobbies: List[str] = None
    interests: List[str] = None
    favorite_music: List[str] = None
    favorite_movies: List[str] = None
    favorite_books: List[str] = None

    def __post_init__(self):
        if self.dietary is None:
            self.dietary = []
        if self.hobbies is None:
            self.hobbies = []
        if self.interests is None:
            self.interests = []
        if self.favorite_music is None:
            self.favorite_music = []
        if self.favorite_movies is None:
            self.favorite_movies = []
        if self.favorite_books is None:
            self.favorite_books = []

@dataclass
class PersonData:
    body: PersonBody
    """
    Hold an PersonBody obj so that we can have ac ess to users physical data  
    """
    psycho_map: dict
    """
    UNDER CONSTRUCTION
    """
    citizenship: PersonCitizenship
    """
    The user legal data.
    """

    contact_info: ContactInfo
    medical_info: MedicalInfo
    employment_info: EmploymentInfo
    social_info: SocialInfo
    preferences: PersonPreferences

class Person:
    """
    User OBJ. can get users save them create them store them. etc
    """
    name: str
    data: PersonData
    tags: list[list[str]]
    """
    The user tags 
    """
    id: str
    """
    User id generated with uuid4
    """

    creation_date: datetime
    login_history: List[datetime]

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.creation_date = datetime.now()
        self.last_updated = datetime.now()
        self.login_history = []

    @staticmethod
    def convert_json_to_user(json_str: dict) -> 'Person':
        """
           Convert a JSON string to a Person object.

           Args:
               json_str: A JSON string representation of a Person object

           Returns:
               A Person object created from the JSON data
           """
        data_dict = json_str

        body = PersonBody(
            gender=PersonGender(data_dict["data"]["body"]["gender"]),
            age=data_dict["data"]["body"]["age"],
            height=data_dict["data"]["body"]["height"],
            weight=data_dict["data"]["body"]["weight"]
        )

        citizenship = PersonCitizenship(
            birth=datetime.fromisoformat(data_dict["data"]["citizenship"]["birth"]),
            name=data_dict["data"]["citizenship"]["name"],
            nationality=data_dict["data"]["citizenship"]["nationality"]
        )

        contact_info = ContactInfo(
            email=data_dict["data"]["contact_info"]["email"],
            phone=data_dict["data"]["contact_info"]["phone"],
            address=data_dict["data"]["contact_info"]["address"],
            city=data_dict["data"]["contact_info"]["city"],
            state=data_dict["data"]["contact_info"]["state"],
            postal_code=data_dict["data"]["contact_info"]["postal_code"],
            country=data_dict["data"]["contact_info"]["country"],
            emergency_contact_name=data_dict["data"]["contact_info"]["emergency_contact_name"],
            emergency_contact_phone=data_dict["data"]["contact_info"]["emergency_contact_phone"]
        )

        blood_type = data_dict["data"]["medical_info"]["blood_type"]
        last_physical_exam = data_dict["data"]["medical_info"]["last_physical_exam"]

        medical_info = MedicalInfo(
            blood_type=BloodType(blood_type) if blood_type else None,
            allergies=data_dict["data"]["medical_info"]["allergies"],
            medications=data_dict["data"]["medical_info"]["medications"],
            medical_conditions=data_dict["data"]["medical_info"]["medical_conditions"],
            insurance_provider=data_dict["data"]["medical_info"]["insurance_provider"],
            insurance_policy_number=data_dict["data"]["medical_info"]["insurance_policy_number"],
            last_physical_exam=datetime.fromisoformat(last_physical_exam) if last_physical_exam else None,
            vaccination_history={k: datetime.fromisoformat(v) for k, v in
                                 data_dict["data"]["medical_info"]["vaccination_history"].items()}
        )

        start_date = data_dict["data"]["employment_info"]["start_date"]

        employment_info = EmploymentInfo(
            status=EmploymentStatus(data_dict["data"]["employment_info"]["status"]),
            current_employer=data_dict["data"]["employment_info"]["current_employer"],
            job_title=data_dict["data"]["employment_info"]["job_title"],
            start_date=datetime.fromisoformat(start_date) if start_date else None,
            salary=data_dict["data"]["employment_info"]["salary"],
            work_history=data_dict["data"]["employment_info"]["work_history"]
        )

        relationships = []
        for rel_data in data_dict["data"]["social_info"]["relationships"]:
            start_date = rel_data.get("start_date")
            rel = Relationship(
                person_id=rel_data["person_id"],
                relationship_type=RelationshipType(rel_data["relationship_type"]),
                start_date=datetime.fromisoformat(start_date) if start_date else None,
                notes=rel_data["notes"]
            )
            relationships.append(rel)

        social_info = SocialInfo(
            marital_status=MaritalStatus(data_dict["data"]["social_info"]["marital_status"]),
            relationships=relationships,
            social_media_accounts=data_dict["data"]["social_info"]["social_media_accounts"]
        )

        preferences = PersonPreferences(
            dietary=data_dict["data"]["preferences"]["dietary"],
            hobbies=data_dict["data"]["preferences"]["hobbies"],
            interests=data_dict["data"]["preferences"]["interests"],
            favorite_music=data_dict["data"]["preferences"]["favorite_music"],
            favorite_movies=data_dict["data"]["preferences"]["favorite_movies"],
            favorite_books=data_dict["data"]["preferences"]["favorite_books"]
        )

        person_data = PersonData(
            body=body,
            psycho_map=data_dict["data"]["psycho_map"],
            citizenship=citizenship,
            contact_info=contact_info,
            medical_info=medical_info,
            employment_info=employment_info,
            social_info=social_info,
            preferences=preferences
        )

        # Create the Person object
        person = Person()
        person.name = data_dict["name"]
        person.id = data_dict["id"]
        person.tags = data_dict["tags"]
        person.creation_date = datetime.fromisoformat(data_dict["creation_date"])
        person.last_updated = datetime.fromisoformat(data_dict["last_updated"])
        person.login_history = [datetime.fromisoformat(dt) for dt in data_dict["login_history"]]
        person.data = person_data

        return person

    @staticmethod
    def load_partial(data_dict: dict) -> 'Person':
        """
        Load a Person object from a JSON string, handling missing fields gracefully.
        This method is designed to work with older versions of the schema that may have fewer fields.

        Args:
            data_dict: A JSON string representation of a Person object

        Returns:
            A Person object created from the JSON data, with default values for missing fields
        """
        person = Person()

        person.name = data_dict.get("name", "")
        person.id = data_dict.get("id", str(uuid.uuid4()))
        person.tags = data_dict.get("tags", [])

        try:
            person.creation_date = datetime.fromisoformat(data_dict.get("creation_date"))
        except (TypeError, ValueError):
            person.creation_date = datetime.now()

        try:
            person.last_updated = datetime.fromisoformat(data_dict.get("last_updated"))
        except (TypeError, ValueError):
            person.last_updated = datetime.now()

        person.login_history = []
        for dt_str in data_dict.get("login_history", []):
            try:
                person.login_history.append(datetime.fromisoformat(dt_str))
            except (TypeError, ValueError):
                continue  # Skip invalid datetime entries

        data = data_dict.get("data", {})

        body_data = data.get("body", {})
        gender_str = body_data.get("gender")
        try:
            gender = PersonGender(gender_str) if gender_str else PersonGender.MALE
        except ValueError:
            gender = PersonGender.MALE

        body = PersonBody(
            gender=gender,
            age=body_data.get("age", 0),
            height=body_data.get("height", 0),
            weight=body_data.get("weight", 0)
        )

        citizenship_data = data.get("citizenship", {})
        birth_str = citizenship_data.get("birth")
        try:
            birth = datetime.fromisoformat(birth_str) if birth_str else datetime.now()
        except (TypeError, ValueError):
            birth = datetime.now()

        citizenship = PersonCitizenship(
            birth=birth,
            name=citizenship_data.get("name", ""),
            nationality=citizenship_data.get("nationality", "")
        )

        contact_data = data.get("contact_info", {})
        contact_info = ContactInfo(
            email=contact_data.get("email", ""),
            phone=contact_data.get("phone", ""),
            address=contact_data.get("address", ""),
            city=contact_data.get("city", ""),
            state=contact_data.get("state", ""),
            postal_code=contact_data.get("postal_code", ""),
            country=contact_data.get("country", ""),
            emergency_contact_name=contact_data.get("emergency_contact_name", ""),
            emergency_contact_phone=contact_data.get("emergency_contact_phone", "")
        )

        medical_data = data.get("medical_info", {})
        blood_type_str = medical_data.get("blood_type")
        try:
            blood_type = BloodType(blood_type_str) if blood_type_str else None
        except ValueError:
            blood_type = None

        last_physical_exam_str = medical_data.get("last_physical_exam")
        try:
            last_physical_exam = datetime.fromisoformat(last_physical_exam_str) if last_physical_exam_str else None
        except (TypeError, ValueError):
            last_physical_exam = None

        # Handle vaccination history
        vaccination_history = {}
        for vaccine, date_str in medical_data.get("vaccination_history", {}).items():
            try:
                vaccination_history[vaccine] = datetime.fromisoformat(date_str)
            except (TypeError, ValueError):
                continue  # Skip invalid entries

        medical_info = MedicalInfo(
            blood_type=blood_type,
            allergies=medical_data.get("allergies", []),
            medications=medical_data.get("medications", []),
            medical_conditions=medical_data.get("medical_conditions", []),
            insurance_provider=medical_data.get("insurance_provider", ""),
            insurance_policy_number=medical_data.get("insurance_policy_number", ""),
            last_physical_exam=last_physical_exam,
            vaccination_history=vaccination_history
        )

        employment_data = data.get("employment_info", {})
        status_str = employment_data.get("status")
        try:
            status = EmploymentStatus(status_str) if status_str else EmploymentStatus.UNEMPLOYED
        except ValueError:
            status = EmploymentStatus.UNEMPLOYED

        start_date_str = employment_data.get("start_date")
        try:
            start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        except (TypeError, ValueError):
            start_date = None

        employment = EmploymentInfo(
            status=status,
            current_employer=employment_data.get("current_employer", ""),
            job_title=employment_data.get("job_title", ""),
            start_date=start_date,
            salary=employment_data.get("salary", 0.0),
            work_history=employment_data.get("work_history", [])
        )

        social_data = data.get("social_info", {})
        marital_status_str = social_data.get("marital_status")
        try:
            marital_status = MaritalStatus(marital_status_str) if marital_status_str else MaritalStatus.SINGLE
        except ValueError:
            marital_status = MaritalStatus.SINGLE

        relationships = []
        for rel_data in social_data.get("relationships", []):
            relationship_type_str = rel_data.get("relationship_type")
            try:
                relationship_type = RelationshipType(
                    relationship_type_str
                ) if relationship_type_str else RelationshipType.OTHER
            except ValueError:
                relationship_type = RelationshipType.OTHER

            start_date_str = rel_data.get("start_date")
            try:
                rel_start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
            except (TypeError, ValueError):
                rel_start_date = None

            rel = Relationship(
                person_id=rel_data.get("person_id", ""),
                relationship_type=relationship_type,
                start_date=rel_start_date,
                notes=rel_data.get("notes", "")
            )
            relationships.append(rel)

        social = SocialInfo(
            marital_status=marital_status,
            relationships=relationships,
            social_media_accounts=social_data.get("social_media_accounts", {})
        )

        preferences_data = data.get("preferences", {})
        preferences = PersonPreferences(
            dietary=preferences_data.get("dietary", []),
            hobbies=preferences_data.get("hobbies", []),
            interests=preferences_data.get("interests", []),
            favorite_music=preferences_data.get("favorite_music", []),
            favorite_movies=preferences_data.get("favorite_movies", []),
            favorite_books=preferences_data.get("favorite_books", [])
        )

        person.data = PersonData(
            body=body,
            psycho_map=data.get("psycho_map", {}),
            citizenship=citizenship,
            contact_info=contact_info,
            medical_info=medical_info,
            employment_info=employment,
            social_info=social,
            preferences=preferences
        )

        return person

    @staticmethod
    def load(user_json: dict) -> 'Person':
        try:
            return Person.convert_json_to_user(user_json)
        except KeyError:
            return Person.load_partial(user_json)

    @staticmethod
    def to_json(person: 'Person'):
        """
        Saves a given user obj to the server
        :param person: The user obj
        """

        user_json = {
            "name": person.name,
            "id": person.id,
            "tags": person.tags,
            "creation_date": person.creation_date.isoformat(),
            "last_updated": person.last_updated.isoformat(),
            "login_history": [dt.isoformat() for dt in person.login_history],
            "data": {
                "body": {
                    "gender": person.data.body.gender.value,
                    "age": person.data.body.age,
                    "height": person.data.body.height,
                    "weight": person.data.body.weight
                },
                "psycho_map": person.data.psycho_map,
                "citizenship": {
                    "birth": person.data.citizenship.birth.isoformat(),
                    "name": person.data.citizenship.name,
                    "nationality": person.data.citizenship.nationality
                },
                "contact_info": {
                    "email": person.data.contact_info.email,
                    "phone": person.data.contact_info.phone,
                    "address": person.data.contact_info.address,
                    "city": person.data.contact_info.city,
                    "state": person.data.contact_info.state,
                    "postal_code": person.data.contact_info.postal_code,
                    "country": person.data.contact_info.country,
                    "emergency_contact_name": person.data.contact_info.emergency_contact_name,
                    "emergency_contact_phone": person.data.contact_info.emergency_contact_phone
                },
                "medical_info": {
                    "blood_type": person.data.medical_info.blood_type.value if person.data.medical_info.blood_type else None,
                    "allergies": person.data.medical_info.allergies,
                    "medications": person.data.medical_info.medications,
                    "medical_conditions": person.data.medical_info.medical_conditions,
                    "insurance_provider": person.data.medical_info.insurance_provider,
                    "insurance_policy_number": person.data.medical_info.insurance_policy_number,
                    "last_physical_exam": person.data.medical_info.last_physical_exam.isoformat() if person.data.medical_info.last_physical_exam else None,
                    "vaccination_history": {vaccine: date.isoformat() for vaccine, date in
                                            person.data.medical_info.vaccination_history.items()}
                },
                "employment_info": {
                    "status": person.data.employment_info.status.value,
                    "current_employer": person.data.employment_info.current_employer,
                    "job_title": person.data.employment_info.job_title,
                    "start_date": person.data.employment_info.start_date.isoformat() if person.data.employment_info.start_date else None,
                    "salary": person.data.employment_info.salary,
                    "work_history": person.data.employment_info.work_history
                },
                "social_info": {
                    "marital_status": person.data.social_info.marital_status.value,
                    "relationships": [
                        {
                            "person_id": rel.person_id,
                            "relationship_type": rel.relationship_type.value,
                            "start_date": rel.start_date.isoformat() if rel.start_date else None,
                            "notes": rel.notes
                        } for rel in person.data.social_info.relationships
                    ],
                    "social_media_accounts": person.data.social_info.social_media_accounts
                },
                "preferences": {
                    "dietary": person.data.preferences.dietary,
                    "hobbies": person.data.preferences.hobbies,
                    "interests": person.data.preferences.interests,
                    "favorite_music": person.data.preferences.favorite_music,
                    "favorite_movies": person.data.preferences.favorite_movies,
                    "favorite_books": person.data.preferences.favorite_books
                }
            }
        }

        return user_json

    def is_birthday(self):
        """
        Check if today is the user birthday
        :return: True if users birthday is today otherwise False
        """
        user_birth = self.data.citizenship.birth
        now = datetime.now()
        return user_birth.day == now.day and user_birth.month == now.month

    def distance_to_birthday(self):
        """
        Returns number of days to birthday
        :return: Integers representing distance in days to next birthday.
        """
        birthday = self.data.citizenship.birth
        now = datetime.now()

        if birthday.month <= now.month and birthday.day < now.day:
            next_birthday = birthday.replace(year=now.year + 1)
        else:
            next_birthday = birthday.replace(year=now.year)
        distance = next_birthday - now

        return distance

    def is_under_age(self):
        """
        Check if the user is under age
        TODO: Add country specific ageing system like US is 20
        :return: True if user is an legal adult
        """
        return self.data.body.age < 18

    def age_in_years(self):
        """
        Returns the age of the person in years
        :return: Integer representing age in years
        """
        return self.data.body.age

    def age_in_months(self):
        """
        Returns the age of the person in months
        :return: Integer representing age in months
        """
        birth_date = self.data.citizenship.birth
        now = datetime.now()
        return (now.year - birth_date.year) * 12 + (now.month - birth_date.month)

    def age_in_days(self):
        """
        Returns the age of the person in days
        :return: Integer representing age in days
        """
        birth_date = self.data.citizenship.birth
        now = datetime.now()
        return (now - birth_date).days

    def calculate_age_at_date(self, target_date: datetime):
        """
        Calculates the age of the person at a specific date
        :param target_date: Datetime object representing the target date
        :return: Integer representing the age at the target date
        """
        birth_date = self.data.citizenship.birth
        age = target_date.year - birth_date.year

        # Check if birthday has occurred this year
        if (target_date.month, target_date.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    def days_until_age(self, target_age):
        """
        Calculates the number of days until the person reaches a specific age
        :param target_age: Integer representing the target age
        :return: Integer representing the number of days until the target age
        """
        birth_date = self.data.citizenship.birth
        target_date = birth_date.replace(year=birth_date.year + target_age)
        now = datetime.now()

        if target_date < now:
            return 0

        return (target_date - now).days

    def get_age_group(self):
        """
        Returns the age group of the person
        :return: String representing the age group
        """
        age = self.age_in_years()
        if age < 13:
            return "Child"
        elif age < 18:
            return "Teenager"
        elif age < 30:
            return "Young Adult"
        elif age < 50:
            return "Adult"
        elif age < 65:
            return "Middle-aged"
        else:
            return "Senior"

    def zodiac_sign(self):
        """
        Returns the zodiac sign of the person based on their birth date
        :return: String representing the zodiac sign
        """
        birth_date = self.data.citizenship.birth
        month = birth_date.month
        day = birth_date.day

        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        else:
            return "Pisces"

    def chinese_zodiac(self):
        """
        Returns the Chinese zodiac sign of the person based on their birth year
        :return: String representing the Chinese zodiac sign
        """
        birth_year = self.data.citizenship.birth.year
        zodiac_animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster",
                          "Dog", "Pig"]
        return zodiac_animals[(birth_year - 1900) % 12]

    def is_male(self):
        """
        Check if the user is of gender male.
        :return: True if its a male otherwise False
        """
        return self.data.body.gender == PersonGender.MALE

    def first_name(self):
        return self.name.split()[0]

    def last_name(self):
        return self.name.split()[-1]

    def full_name(self):
        """
        Returns the full name of the person
        :return: String containing the full name
        """
        return self.name

    def middle_name(self):
        """
        Returns the middle name(s) of the person if they exist
        :return: String containing middle name(s) or empty string if none
        """
        name_parts = self.name.split()
        if len(name_parts) <= 2:
            return ""
        return " ".join(name_parts[1:-1])

    def has_middle_name(self):
        """
        Checks if the person has a middle name
        :return: Boolean indicating if the person has a middle name
        """
        return len(self.name.split()) > 2

    def initials(self):
        """
        Returns the initials of the person
        :return: String containing the initials
        """
        return "".join([name[0].upper() for name in self.name.split()])

    def add_medical_info(self, blood_type=None, allergies=None, medications=None, conditions=None,
                         insurance_provider=None, policy_number=None, last_physical=None):
        """
        Adds or updates medical information for the person
        :param blood_type: BloodType enum value
        :param allergies: List of strings representing allergies
        :param medications: List of strings representing medications
        :param conditions: List of strings representing medical conditions
        :param insurance_provider: String representing insurance provider
        :param policy_number: String representing insurance policy number
        :param last_physical: Datetime object representing the last physical exam date
        :return: None
        """
        if blood_type is not None:
            self.data.medical_info.blood_type = blood_type
        if allergies is not None:
            self.data.medical_info.allergies.extend(allergies)
        if medications is not None:
            self.data.medical_info.medications.extend(medications)
        if conditions is not None:
            self.data.medical_info.medical_conditions.extend(conditions)
        if insurance_provider is not None:
            self.data.medical_info.insurance_provider = insurance_provider
        if policy_number is not None:
            self.data.medical_info.insurance_policy_number = policy_number
        if last_physical is not None:
            self.data.medical_info.last_physical_exam = last_physical

    def add_vaccination(self, vaccine_name, date=None):
        """
        Adds a vaccination to the person's medical records
        :param vaccine_name: String representing the name of the vaccine
        :param date: Datetime object representing the date of vaccination
        :return: None
        """
        self.data.medical_info.vaccination_history[vaccine_name] = date or datetime.now()

    def has_allergy(self, allergen):
        """
        Checks if the person has a specific allergy
        :param allergen: String representing the allergen
        :return: Boolean indicating if the person has the allergy
        """
        return allergen.lower() in [a.lower() for a in self.data.medical_info.allergies]

    def add_employment(self, status=None, employer=None, job_title=None, start_date=None, salary=None,
                       work_history_item=None):
        """
        Adds or updates employment information for the person
        :param status: EmploymentStatus enum value
        :param employer: String representing the current employer
        :param job_title: String representing the job title
        :param start_date: Datetime object representing the start date
        :param salary: Float representing the salary
        :param work_history_item: Dictionary containing work history information
        :return: None
        """
        if status is not None:
            self.data.employment_info.status = status
        if employer is not None:
            self.data.employment_info.current_employer = employer
        if job_title is not None:
            self.data.employment_info.job_title = job_title
        if start_date is not None:
            self.data.employment_info.start_date = start_date
        if salary is not None:
            self.data.employment_info.salary = salary
        if work_history_item is not None:
            self.data.employment_info.work_history.append(work_history_item)

    def years_of_experience(self):
        """
        Calculates the total years of work experience
        :return: Float representing years of experience
        """
        total_days = 0
        for job in self.data.employment_info.work_history:
            if "start_date" in job and "end_date" in job:
                start = job["start_date"] if isinstance(job["start_date"], datetime) else datetime.strptime(
                    job["start_date"], "%d/%m/%Y"
                )
                end = job["end_date"] if isinstance(job["end_date"], datetime) else datetime.strptime(
                    job["end_date"], "%d/%m/%Y"
                )
                total_days += (end - start).days

        if self.data.employment_info.start_date:
            total_days += (datetime.now() - self.data.employment_info.start_date).days

        return round(total_days / 365.25, 1)

    def add_relationship(self, person_id, relationship_type, start_date=None, notes=""):
        """
        Adds a relationship to the person's social info
        :param person_id: String representing the ID of the related person
        :param relationship_type: RelationshipType enum value
        :param start_date: Datetime object representing the start date of the relationship
        :param notes: String containing notes about the relationship
        :return: None
        """
        relationship = Relationship(person_id, relationship_type, start_date, notes)
        self.data.social_info.relationships.append(relationship)

    def update_marital_status(self, status):
        """
        Updates the marital status of the person
        :param status: MaritalStatus enum value
        :return: None
        """
        self.data.social_info.marital_status = status

    def add_social_media(self, platform, username):
        """
        Adds a social media account to the person's social info
        :param platform: String representing the social media platform
        :param username: String representing the username on the platform
        :return: None
        """
        self.data.social_info.social_media_accounts[platform] = username

    def update_preferences(self, dietary=None, hobbies=None, interests=None, music=None, movies=None, books=None):
        """
        Updates the preferences of the person
        :param dietary: List of strings representing dietary preferences
        :param hobbies: List of strings representing hobbies
        :param interests: List of strings representing interests
        :param music: List of strings representing favorite music
        :param movies: List of strings representing favorite movies
        :param books: List of strings representing favorite books
        :return: None
        """
        if dietary is not None:
            self.data.preferences.dietary.extend(dietary)
        if hobbies is not None:
            self.data.preferences.hobbies.extend(hobbies)
        if interests is not None:
            self.data.preferences.interests.extend(interests)
        if music is not None:
            self.data.preferences.favorite_music.extend(music)
        if movies is not None:
            self.data.preferences.favorite_movies.extend(movies)
        if books is not None:
            self.data.preferences.favorite_books.extend(books)

    def log_login(self):
        """
        Logs a login for the person
        :return: None
        """
        self.login_history.append(datetime.now())

    def days_since_last_login(self):
        """
        Calculates the number of days since the last login
        :return: Integer representing days since last login
        """
        if not self.login_history:
            return None

        last_login = self.login_history[-1]
        return (datetime.now() - last_login).days

    def update_contact_info(self, email=None, phone=None, address=None, city=None, state=None, postal_code=None,
                            country=None,
                            emergency_contact_name=None, emergency_contact_phone=None):
        """
        Updates the contact information of the person
        :param email: String representing the email address
        :param phone: String representing the phone number
        :param address: String representing the address
        :param city: String representing the city
        :param state: String representing the state or province
        :param postal_code: String representing the postal code
        :param country: String representing the country
        :param emergency_contact_name: String representing the emergency contact name
        :param emergency_contact_phone: String representing the emergency contact phone number
        :return: None
        """
        if email is not None:
            self.data.contact_info.email = email
        if phone is not None:
            self.data.contact_info.phone = phone
        if address is not None:
            self.data.contact_info.address = address
        if city is not None:
            self.data.contact_info.city = city
        if state is not None:
            self.data.contact_info.state = state
        if postal_code is not None:
            self.data.contact_info.postal_code = postal_code
        if country is not None:
            self.data.contact_info.country = country
        if emergency_contact_name is not None:
            self.data.contact_info.emergency_contact_name = emergency_contact_name
        if emergency_contact_phone is not None:
            self.data.contact_info.emergency_contact_phone = emergency_contact_phone

    def get_full_address(self):
        """
        Returns the full address of the person
        :return: String representing the full address
        """
        address_parts = [
            self.data.contact_info.address,
            self.data.contact_info.city,
            self.data.contact_info.state,
            self.data.contact_info.postal_code,
            self.data.contact_info.country
        ]
        return ", ".join([part for part in address_parts if part])

    def add_tag(self, tag_category, tag_value):
        """
        Adds a tag to the person
        :param tag_category: String representing the tag category
        :param tag_value: String representing the tag value
        :return: None
        """
        self.tags.append([tag_category, tag_value])

    def remove_tag(self, tag_category, tag_value):
        """
        Removes a tag from the person
        :param tag_category: String representing the tag category
        :param tag_value: String representing the tag value
        :return: Boolean indicating if the tag was removed
        """
        for i, tag_list in enumerate(self.tags):
            if tag_list[0] == tag_category and tag_value in tag_list[1:]:
                tag_list.remove(tag_value)
                # If the tag list is now empty (just the category), remove it
                if len(tag_list) == 1:
                    self.tags.pop(i)
                return True
        return False

    def has_tag(self, tag_category, tag_value=None):
        """
        Checks if the person has a specific tag
        :param tag_category: String representing the tag category
        :param tag_value: String representing the tag value (optional)
        :return: Boolean indicating if the person has the tag
        """
        for tag_list in self.tags:
            if tag_list[0] == tag_category:
                if tag_value is None:
                    return True
                return tag_value in tag_list[1:]
        return False

    def get_all_tags(self):
        """
        Gets all tags grouped by category
        :return: Dictionary with categories as keys and lists of tag values as values
        """
        result = {}
        for tag_list in self.tags:
            if tag_list:  # Ensure the list is not empty
                result[tag_list[0]] = tag_list[1:]
        return result

    def export_contact_card(self, filename="contact_card.vcf"):
        """
        Exports the person's contact information as a VCF file
        :param filename: String representing the filename
        :return: None
        """
        vcard = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{self.last_name()};{self.first_name()};;;",
            f"FN:{self.name}",
            f"BDAY:{self.data.citizenship.birth.strftime('%Y%m%d')}",
            f"EMAIL:{self.data.contact_info.email}",
            f"TEL:{self.data.contact_info.phone}",
            f"ADR:;;{self.data.contact_info.address};{self.data.contact_info.city};{self.data.contact_info.state};{self.data.contact_info.postal_code};{self.data.contact_info.country}",
            f"NOTE:Nationality: {self.data.citizenship.nationality}",
            "END:VCARD"
        ]

        with open(filename, "w") as f:
            f.write("\n".join(vcard))
