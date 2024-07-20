from core.skills import BaseSkill

class Hi(BaseSkill):
     def init(self):
          self.register("saudation@hi")
          self.save_responce_for_context = False
          self.can_go_again = False          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("timeOfDay")

          master_name = context.load("master")["name"] # type: ignore

          if self.slot_exists("timeOfDay"):
               self.responce_translated("greet.hi.based.on.time.of.day", {"time": self.slots["timeOfDay"]})
          else:
               self.responce_translated("greet.hi", {"user": master_name})
