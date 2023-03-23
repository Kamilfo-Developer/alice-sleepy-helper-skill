import enum
import datetime
from typing import Union, Optional


class Daytime(enum.Enum):
    DAY = enum.auto()
    NIGHT = enum.auto()
    EVENING = enum.auto()
    MORNING = enum.auto()

    @classmethod
    def from_time(cls, time: Union[datetime.datetime, datetime.time]):
        '''Identify Daytime from time

        Args:
            time (datetime.datetime | datetime.time): time to recieve daytime.

        Returns:
            Daytime: one of daytime options according to the given time
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

    def __init__(self, text: str, tts: Optional[str] = None):
        self.text = text
        if tts is None:
            tts = text
        self.tts = tts


def gentle_capitalize(text: str):
    if not text:
        return text
    return text[0].upper() + text[1:]
