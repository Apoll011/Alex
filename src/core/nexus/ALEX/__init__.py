from core.nexus.ai import AI
from core.system.intents import IntentParserToObject
from .functions import alexSkeleton
from skills.testing.__main__ import EvenOrOdd
from skills.saudation.are_u_sure.__main__ import AreUSure

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
        while True:
            int = input("Seu texto: ")
            promesa = self.api.call_route("intent_recognition/parse", int)
            r = promesa.responce
            t = self.intent.parser(r)
            self.intent.draw_intent(t)
            try:
                EvenOrOdd().execute(self, t)
            except Exception as e:
                print(e)
