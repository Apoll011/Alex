from typing import Any
from core.system.ai.ai import AI
from .functions import alexSkeleton
from core.system.intents.responce import *
from core.system.intents import IntentResponse
from core.system.skills.call import SkillCaller
from core.system.interface.base import BaseInterface, Voice
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
        self.speak("Hi", self.get_context("master")["name"])  # type: ignore
        super().start()

    def loop(self):
        self.interface.loop()
    
    def speak(self, data, voice: str = 'Alex', voice_command = None):
        self.interface.speak(data, voice, voice_command)
        if self.voice_mode:
            Voice().speak(data, voice, voice_command)
    
    def end(self):
        self.interface.close()
    
    def process(self, text) -> (tuple[str, IntentResponse] | tuple[None, IntentResponse]):
        """
            Process a text and execute an action
        """
        if self.next_listen_processor == None:
            return self.process_as_intent(text)
        else:
            
            if self.required_listen_input.is_accepted(text):
                self.next_listen_processor(self.required_listen_input.parse(text), *self.next_processor_args)
                self.next_listen_processor: Any = None
                self.next_processor_args = ()
        return None, self.intentParser.parser({"input": "", "slots": [], "intent": {"intentName": "", "probability": 0}})

    def process_as_intent(self, text) -> (tuple[str, IntentResponse] | tuple[None, IntentResponse]):
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
                return f"An error ocurred during the execution of the intented skill {str(e)}. Please report.", intent
        else:
            return "Sorry. Thats not a valid intent", intent

        return None, intent

    def setListenProcessor(self, callback, responceType, *args):
        self.next_listen_processor = callback
        self.required_listen_input = responceType
        self.next_processor_args = args
