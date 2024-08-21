import json
from enum import Enum

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
         self.name = name
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
              text += f" {self.size.name.lower().replace("x_", "extra ")}"
         
         if self.color != Color.NONE:
              text += f" {self.color.name.lower()}"
         
         text += " {self.name}"
         return text
    
    def json(self):
        j = {
             "name": self.name,
             "atributes": {
                  "color": self.color.value,
                  "size": self.size.value,
                  "quantity": self.quantity,
             }
        }
        return json.dumps(j)

    @staticmethod
    def from_json(itemJsonObj):
       name = itemJsonObj["name"]
       attr = itemJsonObj["atributes"]
       color = Color(attr["color"])
       size = Size(attr["size"])
       quantity = attr["quantity"]

       return Item(name, size, color, quantity)

    def is_name(self, name):
        return self.name.lower() == name.lower()
    
class Lists:
    lists:dict[str, list[Item]] = {}

    def add_to_list(self, list_name: str, item: Item):
        self.ensure_exists(list_name)
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
        return text

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

class ItemOrListDontExist(Exception): ...
class NoElements(Exception):
    def __init__(self, list_name) -> None:
        super().__init__(f"No elements was found on the list {list_name}")
