import time
import datetime


def get_time_of_day():
    """
    Returns either 1, 2 or 3 for the different times of a day: morning, affternon, night. Respectivlly.
    """
    h = datetime.datetime.now().hour
    if h > 18 or h < 7:
        return 3
    elif h >= 12:
        return 2
    elif h >= 7:
        return 1
