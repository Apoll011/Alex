from core.nexus.ai import AI
from .functions import alexSkeleton
from core.system.skills.call import SkillCaller
from core.system.intents import IntentParserToObject
import http.client as httplib
import time

class ALEX(AI):

    internet_is_on: bool

    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.internet_is_on = False
        self.intent = IntentParserToObject()

    def start(self):
        self.clear()
        print("Hi", self.get_context("master")["name"]) # type: ignore
        super().start()

    def loop(self):
        int = self.listen()
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
            self.speak("Sorry. Thats not a valid intent")

    def listen(self):
        if self.internet_is_on:
            time.sleep(1)
            r = super().listen().strip()
        else:
            r = input("Seu texto: ")
        if r == "":
            return self.listen()
        print(r)
        return r

    def internet_on(self):
        connection = httplib.HTTPConnection("google.com",timeout=3)
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return True
        except Exception as exep:
            return False
