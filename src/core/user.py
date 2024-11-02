from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from core.client import ApiMethod
from core.interface import BaseInterface

class UserGender(str, Enum):
    MALE = "M"
    FEMALE = "F"

@dataclass
class UserBody:
    gender: UserGender
    """
    The user gender can be M or F its of type 'UserGender'
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
class UserCitizenship:
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
class UserData:
    body: UserBody
    """
    Hold an UserBody obj so that we can have ac ess to users physical data  
    """
    psycho_map: dict
    """
    UNDER CONSTRUCTION
    """
    citizenship: UserCitizenship
    """
    The user legal data.
    """

class User:
    """
    User OBJ. can get users save them create them store them. etc
    """
    name: str
    data: UserData
    tags: list[list[str]]
    """
    The user tags 
    """
    id: str
    """
    User id generated with uuid4
    """

    @staticmethod
    def search_name(name: str, return_id=False, alex=None) -> list['User'] | list[str]:
        """
        Search a user by its name and return a list of user that match that name
        :param return_id: If set to true return just the list of ids
        :param name: The name to be searched
        :param alex: The Alex Main Class Object its not required if the interface is already set
        :return: List of user with a mathing name
        """
        if alex is None:
            alex = BaseInterface.get().alex

        users_id: list[str] = alex.api.call_route("users/search/name", {"name": name}).response["users"]
        if return_id:
            return [user_id for user_id in users_id]

        return [User.user(user_id, alex) for user_id in users_id]

    @staticmethod
    def user(user_id: str, alex=None) -> 'User':
        """
        Return a user obj based on the given id
        :param user_id: The user ID to retrieve the obj from
        :param alex:  The Alex Main Class Object its not required if the interface is already set
        :return: The user that matches that id
        """
        if alex is None:
            alex = BaseInterface.get().alex
        user = alex.api.call_route("user/", {"id": user_id}).response
        return User.convert_json_to_user(user)

    @staticmethod
    def convert_json_to_user(json: dict) -> 'User':
        """
        Reviews an json containing user data and creates an user object. It will also check the birthday and save the new data to the server.
        :param json: THE user JSON
        :return: An User obj
        """
        user = User()
        user.name = json["name"]
        birth_date = datetime.strptime(json["data"]["citizenship"]["birth"], "%d/%m/%Y")
        user.data = UserData(
            UserBody(
                UserGender(json["data"]["body"]["gender"]),
                int((datetime.now() - birth_date).days / 365),
                json["data"]["body"]["height"],
                json["data"]["body"]["weight"],
            ),
            {},
            UserCitizenship(
                birth_date,
                json["data"]["citizenship"]["name"],
                json["data"]["citizenship"]["nationality"],
            )
        )
        user.tags = json["tags"]
        user.id = json["id"]

        User.save(user)

        return user

    @staticmethod
    def search_tags(query: str, condition: str = ">:0", exclude=None, return_id=False, alex=None) -> list['User'] | \
                                                                                                     list[str]:
        """
        Search a user from a given tag a condition and a list to exclude from
        :param query: The tag to search for
        :param condition: The condition. Created like this (<;>;=;!=;<=;>=):(Strength of that tag 1..100)
        :param exclude: List of users ID to exclude
        :param return_id: If set to true return just the list of ids
        :param alex: The Alex Main Class Object its not required if the interface is already set
        :return: List of user that met that condition
        """
        if alex is None:
            alex = BaseInterface.get().alex

        users_id = alex.api.call_route(
            "users/search/tags",
            {"query": query, "condition": condition, "exclude": [] if exclude is None else exclude}
        ).response["users"]

        if return_id:
            return [user_id for user_id in users_id]

        return [User.user(user_id, alex) for user_id in users_id]

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

    def is_male(self):
        """
        Check if the user is of gender male.
        :return: True if its a male otherwise False
        """
        return self.data.body.gender == UserGender.MALE

    def is_under_age(self):
        """
        Check if the user is under age
        TODO: Add country specific ageing system like US is 20
        :return: True if user is an legal adult
        """
        return self.data.body.age < 18

    @staticmethod
    def save(cls: 'User', alex=None):
        """
        Saves a given user obj to the server
        :param cls: The user obj
        :param alex: The Alex Main Class Object its not required if the interface is already set
        """
        if alex is None:
            alex = BaseInterface.get().alex

        user_json = {
            "id": cls.id,
            "name": cls.name,
            "tags": cls.tags,
            "data": {
                "body": {
                    "age": cls.data.body.age,
                    "gender": cls.data.body.gender.value,
                    "weight": cls.data.body.weight,
                    "height": cls.data.body.height
                },
                "citizenship": {
                    "name": cls.data.citizenship.name,
                    "birth": cls.data.citizenship.birth.strftime("%d/%m/%Y"),
                    "nationality": cls.data.citizenship.nationality

                },
                "psycho_map": cls.data.psycho_map,
            },

        }

        alex.api.call_route("/user/", {"user": user_json}, ApiMethod.PATCH)

    def first_name(self):
        return self.name.split()[0]

    def last_name(self):
        return self.name.split()[-1]
