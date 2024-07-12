from core.skills import BaseSkill

class Tanks(BaseSkill):
     def init(self):
          self.register("saudation@tanks")
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("tank")
