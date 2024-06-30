from core.system.skills.call import SkillCaller
from core.system.skills import BaseSkill

class AreUSure(BaseSkill):
     def __init__(self):
          self.register("saudation@are.u.sure")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)

          last_responce = self.alex_context.load("last_responce")
          last_intent = self.alex_context.load("last_intent")
          
          if last_responce == None:
               self.responce_translated("not.enough.data")
          else:
               skill = SkillCaller().call(last_intent)
               skill.set_as_api()
               new_value = skill.execute(context, last_intent) # type: ignore

               if new_value  == last_responce: 
                    self.responce_translated("confirmation.yes")
               else:
                    self.alex_context.save(new_value, "last_responce")
                    self.responce_translated("confirmation.no", new_value)
                


     def responce(self, text):
          self.speak(text)
