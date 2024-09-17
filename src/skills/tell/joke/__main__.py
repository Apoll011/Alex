from pyjokes import get_joke

from core.skills import BaseSkill

class Joke(BaseSkill):
     def init(self):
          self.register("tell@joke")

     def execute(self, intent):
          super().execute(intent)
          self.optional("jokeType")

          category = self.get("jokeType") if self.slot_exists("jokeType") else "all"
          
          joke = get_joke(category=category)

          self.responce(joke)