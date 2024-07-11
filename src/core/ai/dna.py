import json
from enum import Enum

class DnaAttribute(Enum):
    HAPPINES = "happines"
    AGGRESSIVENESS = "aggressiveness"
    VOICE_SPEED = "voice_speed"
    VOICE_TONE = "voices_tone"
    ATTENTION_TO_DETAIL = "attention_to_detail"
    ADAPTABILITY = "adaptability"
    INITIATIVE = "initiative"
    RACIOCINE_SPEED = "raciocine_speed"
    ACCURACY = "accuracy"
    CONFIDENT = "confident"
    NERVOUS = "nervous"
    IMPATIENT = "impatient"
    SENSITIVE = "sensitive"
    KIND = "kind"
    INSECURE = "insecure"
    CALM = "calm"
    PATIENT = "patient"
    BOLD = "bold"
    SHY = "shy"
    RESPONSIBLE = "responsible"

class AlexDna:
    __dna: dict[str, int]

    def load_dna(self, dna: str):
        dna_object: dict[str, int]  = json.loads(dna)
        self.__dna = dna_object
    
    def get_dna_atribute(self, atribute: DnaAttribute):
        return self.__dna[atribute.value]
    

