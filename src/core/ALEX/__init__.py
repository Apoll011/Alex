import sys
from typing import Any
from core.ai.ai import AI
from .functions import alexSkeleton
from core.intents.responce import *
from core.skills.call import SkillCaller
from core.interface.base import BaseInterface
from core.intents import IntentParserToObject

class ALEX(AI):

    mode: str
    intentParser = IntentParserToObject()

    next_listen_processor: Any = None
    required_listen_input: Responce
    next_processor_args:tuple[Any, ...] = ()

    voice_mode: bool

    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.internet_is_on = False
        self.voice_mode = False
        self.setDefaultListenProcessor()
        
    def start(self):
        self.clear()
    
    def speak(self, data, voice: str = 'Alex', voice_command = None):
        BaseInterface.get().speak(data, voice, voice_command, self.voice_mode | False)
    
    def wake(self, data):
        self.speak({"message": "Yes", "intent": ""})

    def end(self):
        self.speak({"message": "Good bye sir."})
        sys.exit(1)
    
    def process(self, text):
        """
            Process a text and execute an action
        """
        nextL = self.next_listen_processor
        nextA = self.next_processor_args
        
        if self.required_listen_input.is_accepted(text) or self.isListenProcessorDefault():
            self.next_listen_processor(self.required_listen_input.result, *self.next_processor_args)
            if nextL == self.next_listen_processor and nextA == self.next_processor_args:
                self.setDefaultListenProcessor() 
        else:
            return {"message": f"That is not a valid responce for my question. I was expecting {"something with" if not self.required_listen_input.hard_search else ""} {" or ".join(self.required_listen_input.replace.keys())} not {text}", "intent": {}}
        return {"message": "", "intent": {}}

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
                return {"message": f"An error ocurred during the execution of the intented skill {str(e)}. Please report.", "intent": intent}
        else:
            return {"message": "Sorry. Thats not a valid intent", "intent": intent.json}

        return {"message": "", "intent": intent.json}

    def setListenProcessor(self, callback, responceType, *args):
        self.next_listen_processor = callback
        self.required_listen_input = responceType
        self.next_processor_args = args
    
    def setDefaultListenProcessor(self):
        self.next_listen_processor = self.process_as_intent
        self.required_listen_input = AnyResponce()
        self.next_processor_args = ()

    def isListenProcessorDefault(self):
        return self.next_listen_processor == self.process_as_intent
