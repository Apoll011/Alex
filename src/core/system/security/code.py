import datetime
import math
from ._key import AlexKey


class Key:
    @staticmethod
    def get():
        """AlexDayCode"""
        date = datetime.date.today()

        y = date.year
        m = date.month
        d = date.day

        delta_d = 3 * d

        count = ( 
                    ( 
                        ( 
                            (
                                y+math.sqrt(
                                    7*delta_d
                                ) / 2 * y - m
                            ) + (
                                    m ** d - d
                                ) 
                        ) / y - 12 * m + 7 * d 
                    ) / 100**5 + AlexKey.get()
                )
        return f"{count:1f}"