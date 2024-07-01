from core.system.api.client import ApiClient
from core.system.context import ContextManager
from core.system.intents import IntentResponse
from core.system.skills.call import SkillCaller
from core.system.intents import IntentParserToObject

class AiIntentManager:
    intent = IntentParserToObject()    

    api: ApiClient
    debug_mode: bool
    _context: ContextManager

    def process(self, text) -> (tuple[str, IntentResponse] | tuple[None, IntentResponse]):
        """
            Process a text get its intent and run the skill
        """
        promise = self.api.call_route("intent_recognition/parse", text)
        responce = promise.response
        
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
