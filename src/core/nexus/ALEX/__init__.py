import time
import http.client as httplib
from core.nexus.ai import AI
from .functions import alexSkeleton
from core.system.skills.call import SkillCaller
from core.system.intents import IntentParserToObject

class ALEX(AI):

    internet_is_on: bool

    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.internet_is_on = False
        self.server_mode = False
        self.intent = IntentParserToObject()            

    def start(self):
        self.clear()
        print("Hi", self.get_context("master")["name"])  # type: ignore
        super().start()

    def process_message(self, message):
        return self.get_text_and_process(message)

    def loop(self):
        int = self.listen()
        text_returned = self.get_text_and_process(int)
        if text_returned != None:
            self.speak(str(text_returned))

    def get_text_and_process(self, text):
        promesa = self.api.call_route("intent_recognition/parse", text)
        responce = promesa.response
        
        intent = self.intent.parser(responce)
        if intent.intent.intent_name != None:
            if self.debug_mode:
                self.intent.draw_intent(intent)
            try:
                s = SkillCaller().call(intent)
                s.execute(self._context, intent)
            except Exception as e:
                return f"An error ocurred during the execution of the intented skill {str(e)}. Please report.", intent
        else:
            return "Sorry. Thats not a valid intent", intent

        return None, intent
    
    def listen(self):
        if self.internet_is_on:
            time.sleep(1)
            r = super().listen().strip()
        else:
            r = input("Seu texto: ")
        if r == "":
            return self.listen()
        if self.debug_mode:
            print("Input: ", r)
        return r

    def speak(self, text: str, voice: str = 'Alex', voice_command=None):
        if self.debug_mode:
            print("Alex: ", text)
        return super().speak(text, voice, voice_command)

    def internet_on(self):
        connection = httplib.HTTPConnection("google.com",timeout=3)
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return True
        except Exception as exep:
            return False
