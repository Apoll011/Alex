from core.skills import BaseSkill

class Presents(BaseSkill):
     def init(self):
          self.register("alex@presents")
          self.save_responce_for_context = False
          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("alex.how.he.is", {"user": context.load("master")["name"]}) # type: ignore
