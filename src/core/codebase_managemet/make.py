import json
import os

from core.config import LIB_RESOURCE_PATH, RESOURCE_FOLDER, USER_RESOURCE_PATH
from core.resources.application import Application
from core.security.key import AlexKey

class PrepareWorkSpace:
    """
    Create resource folder by:
        MkDIR resources, application, ctx, data
        Download language, model, static, templates

    """

    resources_dirs = [
        "application",
        "ctx",
        "data",
        "users"
    ]

    data_folders = [
        "dict",
        "json",
        "list",
        "log",
        "reminder",
        "txt",
        "temp"
    ]

    base_dna = {
        "happiness": 3.9253765, "aggressiveness": 6.0746235, "voice_speed": 6.514976, "voices_tone": 9.9943083,
        "attention_to_detail": 10.3184173, "adaptability": 2.9211978, "initiative": 2.4117995,
        "raciocine_speed": 9.2752001, "accuracy": 9.5792246, "confident": 2.2259608, "nervous": 0.353407,
        "impatient": 0.3370264, "sensitive": 3.7653402, "kind": 8.098968, "insecure": 0.3353575, "calm": 0.3354233,
        "patient": 2.8654263, "bold": 0.3387997, "shy": 0.3358887, "responsible": 0.9372644
    }

    def __init__(self):
        resource_exists = self.resources_dir_exists()

        if resource_exists:
            return
        else:
            self.generate_resources()
            AlexKey.create()
            self.set_base_dna()

    def generate_resources(self):
        self.create_dirs()

    def resources_dir_exists(self):
        return self.ensure_folder_exists(RESOURCE_FOLDER)

    def create_dirs(self):
        self.ensure_folder_exists(f"{USER_RESOURCE_PATH}/")
        self.ensure_folder_exists(f"{LIB_RESOURCE_PATH}/")
        for dir_name in self.resources_dirs:
            self.ensure_folder_exists(f"{USER_RESOURCE_PATH}/{dir_name}/")

        for data in self.data_folders:
            self.ensure_folder_exists(f"{USER_RESOURCE_PATH}/data/{data}")

    @staticmethod
    def ensure_folder_exists(folder):
        if os.path.isdir(folder):
            return True
        os.mkdir(folder)
        return False

    def set_base_dna(self):
        Application.save("dna", json.dumps(self.base_dna), "a")
