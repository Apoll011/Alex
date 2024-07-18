from core.skills import BaseSkill

class Repeat(BaseSkill):
     def init(self):
          self.register("alex@repeat")
          self.save_responce_for_context = False
          
     def execute(self, context, intent):
          super().execute(context, intent)

          last_responce = self.alex_context.load("last_responce_text")
          
          if last_responce == None:
               self.responce_translated("not.enough.data")
          else:
               self.responce_translated("repeat.text", {"text":last_responce})
