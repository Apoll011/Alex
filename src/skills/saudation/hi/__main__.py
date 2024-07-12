from core.skills import BaseSkill

class Hi(BaseSkill):
     def init(self):
          self.register("saudation@hi")
          self.save_responce_for_context = False
          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("greet.hi", {"user": context.load("master")["name"]}) # type: ignore
