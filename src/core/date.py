import time
import datetime


def get_time_of_day() -> int:
    """
    Returns either 1, 2 or 3 for the different times of a day: morning, affternon, night. Respectivlly.
    """
    h = datetime.datetime.now().hour
    if h >= 7 and h < 12:
        return 1
    elif h >= 12 and h < 18:
        return 2
    elif h >= 18 and h < 7:
        return 3
    return 0
