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
    age: 15
    height: int
    weight: int

@dataclass
class UserCitizenship:
    birth: datetime
    name: str
    nationality: str

@dataclass
class UserData:
    body: UserBody
    psycho_map: dict
    citizenship: UserCitizenship

class User:
    name: str
    data: UserData
    tags: list[list[str]]
    id: str

    @staticmethod
    def search_name(name: str, alex=None) -> list['User']:
        if alex is None:
            alex = BaseInterface.get().alex

        users_id = alex.api.call_route("users/search/name", {"name": name}).response["users"]
        return [User.user(user_id, alex) for user_id in users_id]

    @staticmethod
    def user(user_id: str, alex=None):
        if alex is None:
            alex = BaseInterface.get().alex
        user = alex.api.call_route("user/", {"id": user_id}).response
        return User.convert_json_to_user(user)

    @staticmethod
    def convert_json_to_user(json: dict) -> 'User':
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
    def search_tags(query: str, condition: str = ">:0", exclude=None, alex=None) -> list['User']:
        if alex is None:
            alex = BaseInterface.get().alex

        users_id = alex.api.call_route(
            "users/search/tags",
            {"query": query, "condition": condition, "exclude": [] if exclude is None else exclude}
        ).response["users"]

        return [User.user(user_id, alex) for user_id in users_id]

    def is_birthday(self):
        user_birth = self.data.citizenship.birth
        now = datetime.now()
        return user_birth.day == now.day and user_birth.month == now.month

    def distance_to_birthday(self):
        birthday = self.data.citizenship.birth
        now = datetime.now()

        if birthday.month <= now.month and birthday.day < now.day:
            next_birthday = birthday.replace(year=now.year + 1)
        else:
            next_birthday = birthday.replace(year=now.year)
        distance = next_birthday - now

        return distance

    def is_male(self):
        return self.data.body.gender == UserGender.MALE

    def is_under_age(self):
        return self.data.body.age < 18

    @staticmethod
    def save(cls: 'User', alex=None):
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

        r = alex.api.call_route("/user/", {"user": user_json}, ApiMethod.PATCH)

# {"name": "Tiago Bernardo", "data": {"body": {"gender": "M", "age": 15, "height": 164, "weight": 51}, "psycho_map": {}, "citizenship": {"birth": "16/10/2007", "name": "Tiago Rodrigo Dos Reis Bernardo", "nationality": "Cape Vert"}}, "tags": [["Creator", "100"], ["Friend", "100"], ["Master", "100"]], "id": "f86f0279-c4ec-4f5e-99e9-2fa44059c629"}
