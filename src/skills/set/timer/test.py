from core.system.api.promise.promise import Promise
from core.system.intents.slots import SlotValueDuration
import time

def convertDurationToSeconts(duration: SlotValueDuration):
    s = duration.seconds
    s_m = duration.minutes * 60
    s_h = duration.hours * 60 * 60
    s_d = duration.days * 24 * 60 * 60
    s_w = duration.weeks * 7 * 24 * 60 * 60
    s_mt = duration.months * 30.5 * 24 * 60 * 60
    s_q = duration.quarters * 3 *  30.5 * 24 * 60 * 60
    s_y = duration.years * 365 * 24 * 60 * 60
    return  s + s_m + s_h + s_d + s_w + s_mt + s_q + s_y

d = SlotValueDuration("duration", 0, 0 , 0, 0 , 0, 4, 2, 75, "hour")
print(convertDurationToSeconts(d))
P = Promise()
P.resolve(lambda: time.sleep(2))
P.then(lambda r: print("Ring Ring Ring"))
