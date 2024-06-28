from core.system.api.promise.promise import Promise
from core.system.intents.slots import SlotValueDuration
import time

def total_seconds(duration: SlotValueDuration) -> int:
    """Calculates the total seconds in a SlotValueDuration namedtuple"""
    total_seconds = 0
    total_seconds += duration.years * 365 * 24 * 60 * 60  # assume 365 days per year
    total_seconds += duration.quarters * 3 * 30 * 24 * 60 * 60  # assume 3 months per quarter
    total_seconds += duration.months * 30 * 24 * 60 * 60  # assume 30 days per month
    total_seconds += duration.weeks * 7 * 24 * 60 * 60
    total_seconds += duration.days * 24 * 60 * 60
    total_seconds += duration.hours * 60 * 60
    total_seconds += duration.minutes * 60
    total_seconds += duration.seconds
    return total_seconds

d = SlotValueDuration("duration", 0, 0 , 0, 0 , 0, 4, 2, 75, "hour")
dd = total_seconds(d)
P = Promise()
P.resolve(lambda: time.sleep(2))
P.then(lambda r: print("Ring Ring Ring"))
