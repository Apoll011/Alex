import os
import subprocess

class AiSound:
    """
    A class to interact with the sound system. Plus it's still in construction so we have to use it carefully.
    """
    alex_possibilities = {
        "en_US": "Alex",
        "en_US2": "Fred",
        "en_GB": "Daniel"
    }
    
    alex_voice = alex_possibilities["en_GB"]
    pria_voice = 'Samantha'

    say_voice_command = "say -v '#name#' '#text#'"

    voice_active: bool

    def start(self) -> None:
        """
        Initializes the AiSound instance.
        """
        pass
    def listen(self):
        print("Listening...")
        c = "hear -m -p -t 2"
        result = subprocess.check_output(c, shell=True, text=True)
        return result

    def speak(self, text: str, voice: str = 'Alex', voice_command = None):
        """
        Speaks the given text using the specified voice.

        Args:
            text (str): The text to be spoken.
            voice (str): The voice to use (default: 'Alex').
            voice_command (str): The voice command to use (default: None).
        """
        command = voice_command
        if voice_command is None:
            command = self.say_voice_command
        
        command = command.replace('#name#', voice).replace('#text#', text) # type: ignore

        if self.voice_active:
            os.system(command)
        return text
