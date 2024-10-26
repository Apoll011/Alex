import json

from core.codebase_managemet.app import home
from core.utils import get_skill_config, resource_path

class Config:
    def save_main(self, new_config):
        self.save(f"{home()}/.alex_config", new_config)

    def save_skill(self, name, new_config):
        self.save(f"{resource_path("skills/")}/.alex_config", new_config)

    def save(self, path, content):
        pass

    @staticmethod
    def get_config():
        with open(f"{home()}/.alex_config", "r") as config:
            main_config_file = json.load(config)

        configs = {
            "main": main_config_file,
            "skills": get_skill_config()
        }

        return configs
