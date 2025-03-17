import dataclasses
import json
import os
import uuid
from enum import Enum
from typing import Any, Generator

from core.config import USER_RESOURCE_PATH
from core.users.person import Person

class Symbols(Enum):
    GREATER = ">"
    GREATER_OR_EQUAL = ">="
    SMALLER = ">"
    SMALLER_OR_EQUAL = ">="
    EQUAL = "=="
    NOT_EQUAL = "!="

@dataclasses.dataclass
class Condition:
    symbol: Symbols = ">"
    value: int = 0

    def check(self, number: int):
        match self.symbol:
            case Symbols.GREATER:
                return number > self.value
            case Symbols.GREATER_OR_EQUAL:
                return number >= self.value
            case Symbols.SMALLER:
                return number < self.value
            case Symbols.GREATER_OR_EQUAL:
                return number <= self.value
            case Symbols.EQUAL:
                return number == self.value
            case Symbols.NOT_EQUAL:
                return number != self.value
            case _:
                return False  # If for some God´s sake reason It did not match for any return false. PS: How did we got here???

class PersonsDB:
    users: list[Person] = []
    ids = []

    path = f"{USER_RESOURCE_PATH}/users/"

    def __init__(self) -> None:
        self.update()

    def update(self):
        self.users = []
        for user in os.listdir(self.path):
            us = json.load(open(self.path + user, "r"))
            self.users.append(Person.load(us))
            self.ids.append(us["id"])

    def get(self, user_ids: str | list):
        if user_ids is None:
            return None

        users = []
        for user in self.users:
            if type(user_ids) != list and user.id == user_ids:
                return user
            else:
                users = self.filter_users(user_ids, user.id)
        return users

    @staticmethod
    def filter_users(users_id: list, target_id):
        users = []
        for user_id in users_id:
            if target_id == user_id:
                users.append(user_id)

        return users

    def createUserFunction(self, user_data):
        user = json.loads(user_data.replace("'", '"'))
        user["id"] = str(uuid.uuid4())
        with open(self.path + user["id"] + ".user", "a") as user_file:
            json.dump(user, user_file)

    def createUser(self, user_data):
        self.createUserFunction(user_data=user_data)
        self.update()

    def update_user(self, user_data):
        user = json.loads(user_data.replace("'", '"'))
        with open(self.path + user["id"] + ".user", "w") as ui:
            json.dump(user, ui)
        self.update()

    def delete_user(self, user_id):
        try:
            os.remove(os.path.join(self.path, f"{user_id}.user"))
            self.update()
            return True
        except:
            return False

    def all(self):
        return self.ids

    def search_by_name(self, query):
        for user in self.users:
            if query in user.name:
                yield user

    def search_by_tags(self, query, condition=">:0", exclude=None) -> Generator[Person, Any, None]:
        if exclude is None:
            exclude = []

        condition_parsed = Condition()

        if len(condition.split(":")) >= 1:
            condition_parsed.symbol = Symbols(condition.split(":")[0])
            condition_parsed.value = int(condition.split(":")[1]) if len(condition.split(":")) > 1 else "0"
        for user in self.users:
            if user.id in exclude:
                continue
            else:
                if self.__filter_tags_check_user(user, condition_parsed, query):
                    yield user

    @staticmethod
    def __filter_tags_check_user(user: Person, condition: Condition, query):
        for tag in user.tags:
            query_list: list[str] = query if type(query) == list else [query]  # type: ignore
            for individual_query in query_list:
                if individual_query.lower() == tag[0].lower() and condition.check(int(tag[1])):
                    return True
        return False
