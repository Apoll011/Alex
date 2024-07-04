from typing import Any
from core.system.ai.ai import AI
from .functions import alexSkeleton
from core.system.intents.responce import *
from core.system.skills.call import SkillCaller
from core.system.interface import BaseInterface
from core.system.intents import IntentParserToObject

class ALEX(AI):

    mode: str
    intentParser = IntentParserToObject()

    next_listen_processor: Any = None
    required_listen_input: Responce
    next_processor_args:tuple[Any, ...] = ()

    interface: BaseInterface

    voice_mode: bool


    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.internet_is_on = False
        self.voice_mode = False
        
    def start(self):
        self.clear()
        self.interface.init()
        super().start()

    def loop(self):
        self.interface.loop()
    
    def speak(self, data, voice: str = 'Alex', voice_command = None):
        self.interface.speak(data, voice, voice_command, self.voice_mode)
    
    def wake(self, data):
        self.speak({"message": "Yes", "intent": ""})

    def end(self):
        self.interface.close()
    
    def process(self, text):
        """
            Process a text and execute an action
        """
        if self.next_listen_processor == None:
            return self.process_as_intent(text)
        else:
            if self.required_listen_input.is_accepted(text):
                self.next_listen_processor(self.required_listen_input.result, *self.next_processor_args)
                self.next_listen_processor: Any = None
                self.next_processor_args = ()
            else:
                self.speak({"message": f"That is not a valid responce for my question. I was expecting {"something with" if not self.required_listen_input.hard_search else ""} {" or ".join(self.required_listen_input.replace.keys())} not {text}"})
        return None, self.intentParser.parser({"input": "", "slots": [], "intent": {"intentName": "", "probability": 0}})

    def process_as_intent(self, text):
        promise = self.api.call_route("intent_recognition/parse", text)
        responce = promise.response
        
        intent = self.intentParser.parser(responce)
        if intent.intent.intent_name != None:
            if self.debug_mode:
                self.intentParser.draw_intent(intent)
            try:
                s = SkillCaller().call(intent)
                s.execute(self._context, intent)
            except Exception as e:
                return {"message": f"An error ocurred during the execution of the intented skill {str(e)}. Please report."}, intent
        else:
            return {"message": "Sorry. Thats not a valid intent"}, intent

        return None, intent

    def setListenProcessor(self, callback, responceType, *args):
        self.next_listen_processor = callback
        self.required_listen_input = responceType
        self.next_processor_args = args
