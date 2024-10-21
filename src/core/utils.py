import functools
import warnings

from core.client import ApiResponse
from core.interface import BaseInterface

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
