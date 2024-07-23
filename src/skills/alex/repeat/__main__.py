from core.skills import BaseSkill

class Repeat(BaseSkill):
     def init(self):
          self.register("alex@repeat")
          
     def execute(self, context, intent):
          super().execute(context, intent)

          last_responce = self.alex_context.load("last_responce")
          
          if last_responce == None:
               self.responce_translated("not.enough.data")
          else:
               self.responce_translated("repeat.text", {"text":last_responce})
