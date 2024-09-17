from core.skills import BaseSkill

class RandomName(BaseSkill):
     def init(self):
          self.register("wec@random.name")
          self.save_responce_for_context = False
          self.can_go_again = True

     def execute(self, intent):
         super().execute(intent)
          self.optional("gender")

          if self.slot_exists("gender"):
               name = "Holdon"
          else:
               name = "Hold"

          self.responce_translated("say.name", {"name": name})
