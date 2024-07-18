from core.skills.call import SkillCaller
from core.skills import BaseSkill

class Recall(BaseSkill):
     def init(self):
          self.register("alex@recall")
          self.save_responce_for_context = False
          self.can_go_again = False

     def execute(self, context, intent):
          super().execute(context, intent)

          last_intent = self.alex_context.load("last_intent")
          
          if last_intent == None:
               self.responce_translated("not.enough.data")
          else:
               skill = SkillCaller().call(last_intent) 
               skill.execute(context, last_intent)
