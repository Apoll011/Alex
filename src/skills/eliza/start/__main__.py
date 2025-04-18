from core.eliza import Eliza
from core.skills import BaseSkill

class Start(BaseSkill):
    eliza: Eliza
    def init(self):
        self.register("eliza@start")
        self.can_go_again = False
        self.voice = "Ema"

    def execute(self, intent):
        super().execute(intent)

        self.init_eliza()

        intro = self.eliza.initial()
        self.responce(intro)

        self.on_next_input(self.main_loop)

    def init_eliza(self):
        self.eliza = Eliza()
        self.eliza.memory = self.get_memory()
        script_path = self.get_asset(self.setting("eliza_script")["en"])

        self.eliza.script(script_path)

    def main_loop(self, responce, loop_func=True):
        output = self.eliza.respond(responce)
        self.save_memory()
        if output is None:
            self.responce(self.eliza.final())
        else:
            self.responce(output)
            if loop_func:  # I have to do this cuz the Next listen processor check after Running it. if the next processor remains the same fall back to default.
                self.on_next_input(self.loop)
            else:
                self.on_next_input(self.main_loop)

    def loop(self, responce):
        self.main_loop(responce, False)

    def get_memory(self):
        saved: list[str] | None = self.context_load("eliza_memory")
        if saved is None:
            return []
        else:
            return saved

    def save_memory(self):
        if len(self.eliza.memory) > 0:
            self.context_save("eliza_memory", self.eliza.memory)
