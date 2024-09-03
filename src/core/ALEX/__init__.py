import os
import sys
from typing import Any
from core.error import *
from core.log import LOG
from core.ai.ai import AI
from core.intents import *
from .functions import alexSkeleton
from core.intents.responce import *
from core.date import get_time_of_day
from core.skills.call import SkillCaller
from core.interface.base import BaseInterface

class ALEX(AI):

    mode: str
    intentParser = IntentParserToObject()

    next_listen_processor: Any = None
    required_listen_input: Responce
    next_processor_args:tuple[Any, ...] = ()

    voice_mode: bool

    next_on_loop = None
    next_on_loop_args = None

    def __init__(self) -> None:

        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)

        self.internet_is_on = False
        self.voice_mode = False
        
        self.setDefaultListenProcessor()
        self.start_scheduller()
    
    def interface_on(self):
        self.register_scheduled_funcs()
    
    def set_language(self, lang = "en"):
        self.language = lang
        self.init_translator()
        self.skill_caller = SkillCaller(self.language)

    def start(self):
        self.clear()
    
    def loop(self):
        if self.next_on_loop != None:
            if self.next_on_loop_args:
                self.next_on_loop()
            else:
                self.next_on_loop(*self.next_on_loop_args)
            self.next_on_loop = None
            self.next_on_loop_args = None
    
    def speak(self, data, voice_command = None):
        if BaseInterface.is_set():
            dataP = {
                "type": "say",
                "value": data["message"],
                "settings": {
                    "intent": data["intent"],
                    "voice": data["voice"],
                    "voice_command": voice_command,
                    "voice_mode": self.voice_mode | False
                }
            }
            BaseInterface.get().process(dataP)
        else:
            raise InterfaceNotRegistered()

    def wake(self, data):
        data = {
                "type": "play_audio",
                "value": "./resources/data/mp3/acknowledge.mp3",
                "settings": {
                }
            }
        BaseInterface.get().process(data)
    
    def end(self):
        time_of_day = self.translate(f"time.day.{get_time_of_day()}")
        self.speak(self.make_responce(self.translate("system.close", {"time_of_day": time_of_day})))
        sys.exit(0)
    
    def process(self, text):
        """
            Process a text and execute an action
        """
        if self.required_listen_input.is_accepted(text) or self.isListenProcessorDefault():
            responce =  self.execute_processor()
        else:
            responce = self.wrong_answer(text)
        
        self.speak(responce)
    
    def execute_processor(self) -> dict[str, Any]:
        nextL = self.next_listen_processor
        nextA = self.next_processor_args

        r = self.next_listen_processor(self.required_listen_input.result, *self.next_processor_args)
        if nextL == self.next_listen_processor and nextA == self.next_processor_args:
            self.setDefaultListenProcessor() 
        return r if isinstance(r, dict) else self.make_responce()

    def wrong_answer(self, text):
        joiner = self.translate("wrong.answer.joiner")
        context = {"expected": f" {joiner} ".join(self.required_listen_input.replace.keys()), "entry": text}
        if self.required_listen_input.hard_search:
            return self.translate_responce("wrong.answer.hard", context)
        return self.translate_responce("wrong.answer.soft", context)

    def process_as_intent(self, text):
        promise = self.api.call_route("intent_recognition/", {"text": text})
        responce = promise.response
        
        intent = self.intentParser.parser(responce)
        if intent.intent.intent_name != None:
            if self.debug_mode:
                self.intentParser.draw_intent(intent)
            return self.call_skill(intent)
        else:
            return self.translate_responce("intent.not.valid", intent=intent.json)

    def call_skill(self, intent: IntentResponse):
        try:
            skill = self.skill_caller.call(intent)
            skill.execute(self._context, intent)
            return self.make_responce()
        
        except ModuleNotFoundError:
            return self.translate_responce("error.skill.not.found", {"skill": intent.intent.intent_name}, intent.json)
        except MissingMainSkillClass:
            return self.translate_responce("error.missing.main.skill.class", {"skill": intent.intent.intent_name}, intent.json)
        except SkillIntentError:
            return self.translate_responce("error.wrong.intent", {}, intent.json)
        except SkillSlotNotFound as e:
            return self.translate_responce("error.slot.missing", {"slot": e.slot_name}, intent.json)
        except Exception as e:
            return self.translate_responce("error.during.skill", {"error": str(e)}, intent.json) 

    def setListenProcessor(self, callback, responceType, *args):
        self.next_listen_processor = callback
        self.required_listen_input = responceType
        self.required_listen_input.init()
        self.next_processor_args = args
    
    def setDefaultListenProcessor(self):
        self.next_listen_processor = self.process_as_intent
        self.required_listen_input = AnyResponce()
        self.required_listen_input.init()
        self.next_processor_args = ()

    def isListenProcessorDefault(self):
        return self.next_listen_processor == self.process_as_intent

    def make_responce(self, message = "", intent = {}) -> dict[str, Any]:
        """
        Make a responce spoke by the interface just instancieate witout any args will be a empy responce that wont be spoke by the interface.
        """
        return {"message": message, "intent": intent, "voice": "Alex"}

    def on_next_loop(self, action, *args):
        self.next_on_loop = action
        self.next_on_loop_args = args
