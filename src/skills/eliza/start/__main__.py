from core.skills import BaseSkill
from plugins.eliza import Eliza

class Start(BaseSkill):
     def init(self):
          self.register("eliza@start")
          self.can_go_again = False

     def execute(self, intent):
          super().execute(intent)
          
          self.init_eliza()
          
          intro = self.eliza.initial()
          self.responce(intro)
          
          self.on_next_input(self.main_loop)

     def init_eliza(self):
          self.eliza = Eliza()
          self.eliza.memory = self.get_memory()
          script_path = self.get_asset(self.skill_settings["eliza_script"]["en"])

          self.eliza.script(script_path)

     def main_loop(self, responce, loop_func = True):
          output = self.eliza.respond(responce)
          self.save_memory()
          if output is None:
               self.responce(self.eliza.final())
          else:
               self.responce(output)
               if loop_func: # I have to do this cuz Next listn processor check after Running it if the next processor remains the same fall back to default.
                    self.on_next_input(self.loop)
               else:
                    self.on_next_input(self.main_loop)

     def loop(self, responce):
          self.main_loop(responce, False)

     def get_memory(self):
          saved: list[str] | None = self.alex_context.load("eliza_memory")
          if saved == None:
               return []
          else:
               return saved

     def save_memory(self):
          if len(self.eliza.memory) > 0:
               self.alex_context.save(self.eliza.memory, "eliza_memory")

     def responce(self, text: str):
          self.speak({
               "message": self.process(text),
               "voice": "Ema"
          })

     def process(self, text):
          #Change "'" to something else
          text = text.replace("'", "")
          #Fix spacing 
          return text
