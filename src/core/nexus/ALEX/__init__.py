from core.nexus.ai import AI
from .functions import alexSkeleton
from core.system.skills.call import SkillCaller
from core.system.intents import IntentParserToObject

class ALEX(AI):
    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.intent = IntentParserToObject()

    def start(self):
        self.clear()
        print("Hi", self.get_context("master")["name"]) # type: ignore
        super().start()

    def loop(self):
        int = input("Seu texto: ")
        promesa = self.api.call_route("intent_recognition/parse", int)
        responce = promesa.responce
        intent = self.intent.parser(responce)
        if intent.intent.intent_name != None:
            #Sound().play_dot()
            if self.debug_mode:
                self.intent.draw_intent(intent)
            try:
                s = SkillCaller().call(intent)
                s.execute(self._context, intent)

            except Exception as e:
                print(e)
        else:
            print("Sorry. Thats not a valid intent")
