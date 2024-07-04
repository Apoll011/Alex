from core.system.skills.call import SkillCaller
from core.system.skills import BaseSkill

class Repeat(BaseSkill):
     def __init__(self):
          self.register("alex@repeat")
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)

          last_responce = self.alex_context.load("last_responce_repeater")
          last_intent = self.alex_context.load("last_intent_repeater")
          
          if last_responce == None:
               self.responce_translated("not.enough.data")
          else:
               skill = SkillCaller().call(last_intent) # type: ignore
               skill.execute(context, last_intent) # type: ignore
