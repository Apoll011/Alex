from typing import Any
from core.system.intents.responce import *
from core.system.api.client import ApiClient
from core.system.context import ContextManager
from core.system.intents import IntentResponse
from core.system.skills.call import SkillCaller
from core.system.intents import IntentParserToObject

class AiIntentManager:
    
    intentParser = IntentParserToObject()

    api: ApiClient
    debug_mode: bool
    _context: ContextManager

    next_listen_processor: Any = None
    required_listen_input: Responce
    next_processor_args:tuple[Any, ...] = ()

    def process(self, text) -> (tuple[str, IntentResponse] | tuple[None, IntentResponse]):
        """
            Process a text and execute an action
        """
        print(self.next_listen_processor)
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
