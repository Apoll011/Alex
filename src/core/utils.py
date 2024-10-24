import datetime
import functools
import http.client as httplib
import json
import os
import sys
import warnings

from core.client import ApiResponse
from core.codebase_managemet.app import is_compiled
from core.interface import BaseInterface

def get_time_of_day():
    """
    :return: either 1, 2 or 3 for the different times of a day: morning, afternoon, night. Respectively.
    """
    h = datetime.datetime.now().hour
    if h > 18 or h < 7:
        return 3
    elif h >= 12:
        return 2
    elif h >= 7:
        return 1

def is_morning():
    return get_time_of_day() == 1

def deprecated(msg=""):
    """Decorator factory to mark functions as deprecated with given message.

    >>> @deprecated("Enough!")
    ... def some_function():
    ...    "I just print 'hello world'."
    ...    print("hello world")
    >>> some_function()
    hello world
    >>> some_function.__doc__ == "I just print 'hello world'."
    True
    """

    def deprecated_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} function is a deprecated. {msg}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return deprecated_decorator

def get_meaning_of_word(word: str, closest: bool = True):
    url = "dictionary/get/closest" if closest else "dictionary/get/"
    meaning: ApiResponse = BaseInterface.get().alex.handle_request("sendToApi", url, {"word": word.lower()})

    return meaning.response

def internet_on():
    """
    See if the internet is on or not by sending a request to google.com.
    :return: A boolean
    """
    connection = httplib.HTTPConnection("google.com", timeout=1)
    try:
        # only header requested for fast operation
        connection.request("HEAD", "/")
        connection.close()  # connection closed
        return True
    except Exception:
        return False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except (ModuleNotFoundError, Exception):
        base_path = os.path.abspath("." if is_compiled() else "./src/")

    return os.path.join(base_path, relative_path)

def list_skills():
    major_list = os.listdir(str(resource_path("skills/")))
    try:
        major_list.remove("__pycache__")
    except ValueError:
        pass

    skills = []

    for major in major_list:
        minor_list = os.listdir(str(resource_path(f"skills/{major}")))
        try:
            minor_list.remove("__pycache__")
        except ValueError:
            pass

        for individual in minor_list:
            if os.path.isdir(resource_path(f"skills/{major}/{individual}")):
                skills.append(resource_path(f"skills/{major}/{individual}"))

    return skills

def get_skill_config():
    skills = list_skills()
    sk_conf = []
    for skill in skills:

        try:
            with open(os.path.join(str(skill), ".config"), "r") as config:
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
