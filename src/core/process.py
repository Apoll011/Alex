import time

from core.error import *
from core.intents import *
from core.intents.responce import *
from core.log import LOG
from core.skills.call import SkillCaller

class Process:
    intentParser = IntentParserToObject()

    next_listen_processor: Any = None
    required_listen_input: Responce
    next_processor_args: tuple[Any, ...] = ()
    on_none_responce = None

    id = None

    def __init__(self, alex):
        self.skill_caller = None
        self.debug_mode = alex.debug_mode
        self.api = alex.api
        self.translate = alex.translate
        self.translate_responce = alex.translate_responce
        self.make_responce = alex.make_responce
        self.get_loop_id = alex.get_loop_id
        self.skill_caller = SkillCaller(alex.language)
        self.setDefaultListenProcessor()

    def process(self, text):
        """
            Process a text and execute an action
        """
        try:
            if self.required_listen_input.is_accepted(text) or self.isListenProcessorDefault():
                responce = self.execute_processor()
            else:
                responce = self.wrong_answer(text)

            return responce
        except KeyError:
            return "An error occur while connection to the server please try again."

    def execute_processor(self) -> dict[str, Any]:
        nextL = self.next_listen_processor
        nextA = self.next_processor_args
        # This code might look confusing.
        # Thrust me it is.
        # Explanation:
        # Alex has One WAy of understanding what the user says (Listen_processor)
        # but sometimes a skill might need to get the text a user sends without parsing its intent
        # so they can set their one listen processor for the next loop
        # (User input.)
        args = list(self.next_processor_args)
        try:
            args.remove(None)
        except ValueError:
            pass
        responce = self.next_listen_processor(self.required_listen_input.result, *args)
        if nextL == self.next_listen_processor and nextA == self.next_processor_args:  # After getting the value they wanted
            # (Skill listen processor)
            # they might want
            # to know something else.
            # (That listen processor would be set inside the executing of the previous action,
            # so if this Check is not here, they could not do that)
            self.setDefaultListenProcessor()
        self.save_on_none()
        return responce if isinstance(responce, dict) else self.make_responce()

    def wrong_answer(self, text):
        joiner = self.translate("wrong.answer.joiner")
        context = {"expected": f" {joiner} ".join(self.required_listen_input.replace.keys()), "entry": text}
        if self.required_listen_input.hard_search:
            return self.translate_responce("wrong.answer.hard", context)
        return self.translate_responce("wrong.answer.soft", context)

    def process_as_intent(self, text):
        started = time.time()
        promise = self.api.call_route("intent_recognition/", {"text": text})
        responce = promise.response

        server_time = time.time() - started

        intent = self.intentParser.parser(responce)
        if intent.intent.intent_name is not None:
            if self.debug_mode:
                self.intentParser.draw_intent(intent)
            result = self.call_skill(intent)
        elif self.is_on_none_set():
            result = self.execute_on_none(text)
        else:
            result = self.translate_responce("intent.not.valid", intent=intent.json)

        took = time.time() - started

        if self.debug_mode:
            print("Took:", server_time, "seconds to get intent +", took - server_time, "Of skill execution")

        return result

    def call_skill(self, intent: IntentResponse):
        try:
            skill = self.skill_caller.call(intent)
            skill.execute(intent)
            return self.make_responce()
        except ModuleNotFoundError as e:
            LOG.error(f"Try to call none existing skill {intent.intent.intent_name} {e}")
            return self.translate_responce("error.skill.not.found", {"skill": intent.intent.intent_name}, intent.json)
        except MissingMainSkillClass:
            LOG.error(f"Skill {intent.intent.intent_name} missing main class")
            return self.translate_responce(
                "error.missing.main.skill.class", {"skill": intent.intent.intent_name}, intent.json
            )
        except SkillIntentError:
            return self.translate_responce("error.wrong.intent", {}, intent.json)
        except SkillSlotNotFound as e:
            return self.translate_responce("error.slot.missing", {"slot": e.slot_name}, intent.json)
        except Exception as e:
            LOG.error(e)
            return self.translate_responce("error.during.skill", {"error": str(e)}, intent.json)

    def setListenProcessor(self, callback, responceType, *args):
        self.next_listen_processor = callback
        self.required_listen_input = responceType
        self.required_listen_input.init()
        self.next_processor_args = args
        self.id = self.get_loop_id()

    def setDefaultListenProcessor(self):
        self.id = None
        self.next_listen_processor = self.process_as_intent
        self.required_listen_input = AnyResponce()
        self.required_listen_input.init()
        self.next_processor_args = ()

    def isListenProcessorDefault(self):
        return self.next_listen_processor == self.process_as_intent

    def get_current_listen_processor(self):
        return self.next_listen_processor

    def save_on_none(self):
        if not self.isListenProcessorDefault():
            self.on_none_responce = self.next_listen_processor, self.required_listen_input, self.next_processor_args if len(
                self.next_processor_args
            ) > 0 else None

    def clear_none(self):
        self.on_none_responce = None

    def is_on_none_set(self):
        return True if self.on_none_responce else False

    def execute_on_none(self, text):
        callback, responceType, args = self.on_none_responce
        self.setListenProcessor(callback, responceType, args if args is not None or args != (()) else ())
        if self.required_listen_input.is_accepted(text):
            responce = self.execute_processor()
        else:
            responce = self.wrong_answer(text)

        self.clear_none()
        return responce if isinstance(responce, dict) else self.make_responce()
