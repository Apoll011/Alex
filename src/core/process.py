import time

from core.ai.ai import AI
from core.error import *
from core.intents import *
from core.intents.responce import *
from core.log import LOG
from core.skills.call import SkillCaller

class Process:
    """
    Class used in input processing
    """
    intentParser = IntentParserToObject()
    """
    The intent parser receives a intent json a return an intent obj
    """

    next_listen_processor: Any = None
    """
    The next function that will process an input. The default is None
    """
    required_listen_input: Responce
    """
    What should alex listen for is it a list is it yes or no is it any responce. set it here
    """
    next_processor_args: tuple[Any, ...] = ()
    """
    THe args to pass to the next listen processor
    """
    on_none_responce = None
    """
    If alex don't run this method 
    """

    id: int = None
    """Current Loop ID"""

    def __init__(self, alex: AI):
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
        """
        Will execute the current listen processor and set it back to default if nothing changes.
        :return: The responce returned by the listen processor
        """
        previous_listen_processor = self.next_listen_processor
        previous_listen_processor_args = self.next_processor_args
        args = list(self.next_processor_args)
        if None in args:
            args.remove(None)

        responce = self.next_listen_processor(self.required_listen_input.result, *args)
        if previous_listen_processor == self.next_listen_processor and previous_listen_processor_args == self.next_processor_args:
            self.setDefaultListenProcessor()

        self.set_processor_on_none()

        return self.return_responce_or_default_responce(responce)

    def wrong_answer(self, text):
        """
        Create a responce that tells the user that their responce is wrong.
        :param text: The text spoken
        :return: THe responce obj
        """
        joiner = self.translate("wrong.answer.joiner")
        context = {"expected": f" {joiner} ".join(self.required_listen_input.replace.keys()), "entry": text}
        if self.required_listen_input.hard_search:
            return self.translate_responce("wrong.answer.hard", context)
        return self.translate_responce("wrong.answer.soft", context)

    def process_as_intent(self, text):
        """
        This is the default listen processor this will receive a text get its intent and execute the corresponding skill
        :param text: The input
        :return: The responce by the skill
        """
        started = time.time()

        responce = self.api.call_route("intent_recognition/", {"text": text}).response

        server_time = time.time() - started

        result = self.execute_intent(responce, text)

        took = time.time() - started

        if self.debug_mode:
            print("Took:", server_time, "seconds to get intent +", took - server_time, "Of skill execution")

        return result

    def execute_intent(self, intent, text):
        """
        WIll receive an intent and execute its skill.
        :param text: The input text
        :param intent: The intent json
        :return: THe responce
        """
        intent_obj = self.intentParser.parser(intent)
        if intent_obj.intent.intent_name is not None:
            if self.debug_mode:
                self.intentParser.draw_intent(intent_obj)
            result = self.call_skill(intent_obj)
        elif self.is_on_none_processor_set():
            result = self.execute_on_none(text)
        else:
            result = self.translate_responce("intent.not.valid", intent=intent_obj.json)

        return result

    def call_skill(self, intent: IntentResponse):
        """
        Receives an intent obj and executes its respective skill
        :param intent: THe input intent obj
        :return: THe skill return
        """
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
            LOG.error(
                f"How the heck we get in here as where the skill caller called the wrong skill ({intent.intent.intent_name}). Probably a typo in register."
                )
            return self.translate_responce("error.wrong.intent", {}, intent.json)
        except SkillSlotNotFound as e:
            LOG.error(f"Skill {intent.intent.intent_name} missing-")
            return self.translate_responce("error.slot.missing", {"slot": e.slot_name}, intent.json)
        except Exception as e:
            LOG.error(e)
            return self.translate_responce("error.during.skill", {"error": str(e)}, intent.json)

    def setListenProcessor(self, callback, responceType, *args):
        """
        Method to set the next listen processor
        :param callback: THe function to call on next input
        :param responceType: WHat you want the user saying
        :param args: Args to pass to callback
        """
        self.next_listen_processor = callback
        self.required_listen_input = responceType
        self.required_listen_input.init()
        self.next_processor_args = args
        self.id = self.get_loop_id()

    def setDefaultListenProcessor(self):
        """
        Set the next listen processor as default
        """
        self.setListenProcessor(self.process_as_intent, AnyResponce())
        self.next_processor_args = ()
        self.id = None

    def isListenProcessorDefault(self):
        """
        Returns true if the current listen processor is the default one
        :return: True or False
        """
        return self.next_listen_processor == self.process_as_intent

    def get_current_listen_processor(self):
        """
        Returns the current listen processor
        :return: callable
        """
        return self.next_listen_processor

    def set_processor_on_none(self):
        """
        Set the current processor for the on none property.
        """
        if not self.isListenProcessorDefault():
            self.on_none_responce = self.next_listen_processor, self.required_listen_input, self.next_processor_args if len(
                self.next_processor_args
            ) > 0 else None

    def clear_on_none_processor(self):
        """
        Will clear the on none processor back to None
        """
        self.on_none_responce = None

    def is_on_none_processor_set(self):
        """
        Return true if there is set a on none processor otherwise false
        :return: True or False
        """
        return True if self.on_none_responce else False

    def execute_on_none(self, text):
        """
        Will execute the on not understood method if set and pass the input
        :param text: The input
        :return:
        """
        callback, responceType, args = self.on_none_responce
        self.setListenProcessor(callback, responceType, args if args is not None or args != (()) else ())
        if self.required_listen_input.is_accepted(text):
            responce = self.execute_processor()
        else:
            responce = self.wrong_answer(text)

        self.clear_on_none_processor()
        return self.return_responce_or_default_responce(responce)

    def return_responce_or_default_responce(self, responce):
        """
        Will return the provided responce if valid otherwise return the default responce.
        :param responce: The alex responce from processor
        :return: A valid responce
        """
        return responce if isinstance(responce, dict) else self.make_responce()