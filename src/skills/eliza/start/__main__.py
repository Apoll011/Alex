from core.eliza import Eliza
from core.skills import BaseSkill
from core.resources.data_files import DataFile

class Start(BaseSkill):
     def init(self):
          self.register("eliza@start")
          self.can_go_again = False          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.eliza = Eliza()
          self.eliza.script(DataFile.getPath("eliza.en", "doc"))
          intro = self.eliza.initial()
          self.responce(intro)
          self.on_next_input(self.main_loop)

     def main_loop(self, responce):
          output = self.eliza.respond(responce)
          if output is None:
               self.responce(self.eliza.final())
          else:
               self.responce(output)
               self.on_next_input(self.main_loop)     
