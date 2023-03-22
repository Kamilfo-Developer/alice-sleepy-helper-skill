import enum
import datetime
from typing import Union


class Daytime(enum.Enum):
    DAY = enum.auto()
    NIGHT = enum.auto()
    EVENING = enum.auto()
    MORNING = enum.auto()

    @classmethod
    def from_time(cls, time: Union[datetime.datetime, datetime.time]):
        '''
        Identify Daytime from time
        '''
        if isinstance(time, datetime.datetime):
            time = time.time()
        morning = datetime.time(5, 0, 0)
        day = datetime.time(12, 0, 0)
        evening = datetime.time(16, 0, 0)
        night = datetime.time(23, 0, 0)

        if time < morning:
            return cls.NIGHT
        if time < day:
            return cls.MORNING
        if time < evening:
            return cls.DAY
        if time < night:
            return cls.EVENING
        return cls.NIGHT


class TextWithTTS:
    text: str
    tts: str

    def __init__(self, text: str, tts: str):
        self.text = text
        self.tts = tts
