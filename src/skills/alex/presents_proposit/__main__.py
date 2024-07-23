from core.skills import BaseSkill

class PresentsProposit(BaseSkill):
     def init(self):
          self.register("alex@presents.proposit")
          
     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("alex.proposit")
