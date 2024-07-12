from core.skills import BaseSkill

class PresentsProposit(BaseSkill):
     def init(self):
          self.register("alex@presents.proposit")
          self.save_responce_for_context = False
          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("alex.proposit")
