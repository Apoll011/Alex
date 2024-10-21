import datetime
import functools
import warnings

from core.client import ApiResponse
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
