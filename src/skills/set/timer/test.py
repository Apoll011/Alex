from core.api.promise.promise import Promise
from core.intents.slots import SlotValueDuration
import time
import datetime


def convertDurationToDateTime(duration: SlotValueDuration):
    return datetime.datetime(duration.years, (duration.quarters * 3) + duration.months, (duration.weeks * 7) + duration.days, duration.hours, duration.minutes, duration.minutes)

def getDateTimeToSeconds(datetime: datetime.datetime):
    total_timedelta = datetime - datetime.now()
    return total_timedelta.total_seconds()

d = SlotValueDuration("duration", 0, 0 , 0, 0 , 0, 4, 2, 75, "hour")
dd = convertDurationToDateTime(d)
print
P = Promise()
P.resolve(lambda: time.sleep(2))
P.then(lambda r: print("Ring Ring Ring"))
