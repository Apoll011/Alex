from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from core.interface import BaseInterface

class UserGender(Enum):
    MALE = "M"
    FEMALE = "F"

@dataclass
class UserBody:
    gender: UserGender
    age: 15
    skin_tone: str
    height: int
    weight: int

@dataclass
class UserCitizenship:
    birth: datetime
    name: str
    nacionality: str

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
    def search_name(name: str, alex=None) -> 'User':
        if alex is None:
            alex = BaseInterface.get().alex

        user_id = alex.api.call_route("users/search/name", {"name": "Tiago"}).response["users"][0]
        user = alex.api.call_route("user/", {"id": user_id}).response
        return User.convert_json_to_user(user)

    @staticmethod
    def convert_json_to_user(json):
        user = User()
        user.name = json["name"]
        birth_date = datetime.strptime(json["data"]["citizenship"]["birth"], "%d/%m/%Y")
        user.data = UserData(
            UserBody(
                UserGender(json["data"]["body"]["genner"]),
                int((datetime.now() - birth_date).days / 365),
                json["data"]["body"]["skin_tone"],
                json["data"]["body"]["height"],
                json["data"]["body"]["weight"],
            ),
            {},
            UserCitizenship(
                birth_date,
                json["data"]["citizenship"]["name"],
                json["data"]["citizenship"]["nacionality"],
            )
        )
        user.tags = json["tags"]
        user.id = json["id"]

        return user

    @staticmethod
    def search_tags(query: str, condition: str = ">:0", exclude=None) -> 'User':
        pass

    def is_birthday(self):
        user_birth = self.data.citizenship.birth
        now = datetime.now()
        return user_birth.day == now.day and user_birth.month == now.month

    def is_male(self):
        return self.data.body.gender == UserGender.MALE
