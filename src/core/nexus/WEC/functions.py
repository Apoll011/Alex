from random import choice
from core.system.ai.ai import AI
from core.system.ai.blueprint import AiBluePrintSkeleton



wecSkeleton = AiBluePrintSkeleton()

@wecSkeleton.init_action("Loading Countries")
def load_countries(self, wec: AI):
    content = wec.open_file_in_data_learn("countries.txt").splitlines()
    wec.database["countries"] = content
    wec.finish(self)

@wecSkeleton.init_action("Loading Names")
def load_names(self, wec: AI):
    content_male = wec.open_file_in_data_learn("names/male.txt").splitlines()
    content_female = wec.open_file_in_data_learn("names/female.txt").splitlines()
    wec.database["names"] = {
        "male": content_male,
        "female": content_female
    }
    wec.finish(self)


@wecSkeleton.request_action("getName")
def get_name(wec: AI, gender: str):
    if gender == None:
        return choice(wec.database["names"][choice(["male", "female"])])
    elif gender.lower() == "male" or gender.lower() == "female":
        return choice(wec.database["names"][gender])
    else:
        raise NotAValidGender(f"{gender} is not a valid gender.")

class NotAValidGender(Exception): ...
