from core.skills import BaseSkill

class Presents(BaseSkill):
     def __init__(self):
          self.register("alex@presents")
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("alex.how.he.is", {"user": context.load("master")["name"]}) # type: ignore
