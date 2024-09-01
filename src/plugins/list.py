import json
from enum import Enum
from core.resources.data_files import DataFile

class Size(Enum):
    X_SMALL = -2
    SMALL = -1
    NORMAL = 0
    LARGE = 1
    X_LARGE = 2

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0 , 0)
    WHITE = (255, 255, 255)
    NONE = (-1, -1, -1)

class Item:
    name: str
    size: Size = Size.NORMAL
    color: Color = Color.NONE
    quantity: int = 1

    def __init__(self, name: str, size: Size = Size.NORMAL, color: Color = Color.NONE, quantity: int = 1) -> None:
         self.name = name.lower()
         self.size = size
         self.color = color
         self.quantity = quantity

    def get_representation(self):
         """{Quantity} {size} {color} {name}"""
         text = ""
         if self.quantity != 1:
              text += f" {self.quantity}"
         else:
              text += "An "

         if self.size != Size.NORMAL:
              text += f" {self.size.name.title().replace('x_', 'extra ')}"
         
         if self.color != Color.NONE:
              text += f" {self.color.name.title()}"
         
         text += f" {self.name.title()}"
         return text.strip()
    
    def json(self):
        j = {
             "name": self.name,
             "atributes": {
                  "color": self.color.value,
                  "size": self.size.value,
                  "quantity": self.quantity,
             }
        }
        return j

    @staticmethod
    def from_json(itemJsonObj):
       name = itemJsonObj["name"]
       attr = itemJsonObj["atributes"]
       color = Color(tuple(attr["color"]))
       size = Size(attr["size"])
       quantity = attr["quantity"]

       return Item(name, size, color, quantity)

    def is_name(self, name):
        return self.name.lower() == name.lower()
    
    def is_equal(self, item:'Item'):
        if (self.name.lower() == item.name.lower()) and (self.color == item.color) and (self.size == self.size):
            return True
        return False
    
    def increment(self, quantity: int):
        self.quantity += quantity

class Lists:
    lists:dict[str, list[Item]] = {}

    def add_to_list(self, list_name: str, item: Item):
        self.ensure_exists(list_name)
        for eitem in self.lists[list_name]:
            if eitem.is_equal(item):
                eitem.increment(item.quantity)
                return
        self.lists[list_name].append(item)
    
    def ensure_exists(self, list_name:str):
        if list_name in self.lists.keys():
            return
        else:
            self.lists[list_name] = []

    def get(self, list_name: str, item_name: str = ""):
        self.ensure_exists(list_name)
        if item_name != "":
            return self.get_item(list_name, item_name)
        else:
            return self.get_list(list_name, "and")
    
    def get_item(self, list_name: str, item_name: str):
        for item in self.lists[list_name]:
            if item.is_name(item_name):
                return True
        return False

    def get_list(self, list_name, ander):
        list_content = self.lists[list_name]
        if len(list_content) == 0:
            raise NoElements(list_name)
        elif len(list_content) == 1:
            text = list_content[0].get_representation()
        else:
            text = ", ".join(self.representation_of_all_elements(list_name)[0:-1]) + f" {ander} " + list_content[-1].get_representation()
        return text.replace("  ", " ").strip()

    def representation_of_all_elements(self, list_name) -> list[str]:
        return list(map(lambda x: x.get_representation(), self.lists[list_name]))

    def clear(self, list_name: str, item_name: str = ""):
        self.ensure_exists(list_name)
        if item_name != "":
            self.remove_item(list_name, item_name)
        else:
            self.lists[list_name] = []

    def remove_item(self, list_name: str, item_name):
        try:
            item = self.item(list_name, item_name)
            self.lists[list_name].remove(item)
        except KeyError:
            raise ItemOrListDontExist()
    
    def item(self, list_name, item_name):
        for item in self.lists[list_name]:
            if item.is_name(item_name):
                return item
            
        raise KeyError("This item does not exist")
    
    def update(self, list_name, item_name, item: Item):
        self.remove_item(list_name, item_name)
        self.add_to_list(list_name, item)

    def json(self):
        n_l = {}
        for li in self.lists:
            l = self.lists[li]
            n_l[li] = []
            for i in l:
                n_l[li].append(i.json())
        return n_l
    
    def save(self):
        j = self.json()
        with open(DataFile.getPath("lists", "json"), "w") as file:
            json.dump(j, file)

    @staticmethod
    def load() -> 'Lists':
        l = Lists()

        try:
            with open(DataFile.getPath("lists", "json"), "r") as file:
                list = json.load(file)
            for li in list:
                for item in list[li]:
                    l.add_to_list(li, Item.from_json(item))
        except KeyError:
            pass

        return l

class ItemOrListDontExist(Exception): ...
class NoElements(Exception):
    def __init__(self, list_name) -> None:
        super().__init__(f"No elements was found on the list {list_name}")
