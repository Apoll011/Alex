import json
import os.path

from core.utils import list_skills

def get_skill_config():
    skills = list_skills()
    sk_conf = []
    for skill in skills:

        try:
            with open(os.path.join(skill, ".config"), "r") as config:
                conf = json.load(config)

                if "config" in conf.keys():
                    sk_conf.append(
                        {
                            "name": skill.split("/")[-2:],
                            "config": conf
                        }
                    )


        except KeyError:
            pass
    return sk_conf
