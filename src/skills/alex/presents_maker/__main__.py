from core.skills import BaseSkill

class PresentsMaker(BaseSkill):
     def init(self):
          self.register("alex@presents.maker")
          self.save_responce_for_context = False
          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("who.made.alex", {"creator": self.get_creator()["name"]})

     def get_creator(self):
          user_id = self.alex().api.call_route("users/search/tags", {"query": "Creator"}).response["users"][0]
          user = self.alex().api.call_route("users/get", user_id).response
          return user
