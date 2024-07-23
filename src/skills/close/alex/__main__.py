from core.skills import BaseSkill
from core.interface.base import BaseInterface
from core.intents.responce import BoolResponce

class Alex(BaseSkill):
     def init(self):
          self.register("close@alex")
          self.can_go_again = False

     def execute(self, context, intent):
          super().execute(context, intent)
          self.question("close.server", self.after_responce, {}, BoolResponce())
     
     def after_responce(self, close_server):
          if close_server:
               promise = BaseInterface.get().alex.api.call_route_async("close") 
               promise.catch(lambda x: self.responce_translated(x))
               promise.reject("server.closed")
          BaseInterface.get().alex.deactivate()
