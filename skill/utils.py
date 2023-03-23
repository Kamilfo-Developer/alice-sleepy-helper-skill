from __future__ import annotations
import enum
import datetime
import random
from typing import Union, Any, Iterable, List


class Daytime(enum.Enum):
    DAY = enum.auto()
    NIGHT = enum.auto()
    EVENING = enum.auto()
    MORNING = enum.auto()

    @classmethod
    def from_time(cls, time: Union[datetime.datetime, datetime.time]):
        """Identify Daytime from time

        Args:
            time (datetime.datetime | datetime.time): time to recieve daytime.

        Returns:
            Daytime: one of daytime options according to the given time
        """
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

    def __init__(self, text: str, tts: str | None = None):
        self.text = text
        if tts is None:
            tts = text
        self.tts = tts

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, TextWithTTS)
            and self.text == __o.text
            and self.tts == __o.tts
        )

    def __str__(self) -> str:
        return "Text:\n" f"{self.text}" "\n" "TTS:\n" f"{self.tts}"

    def __add__(self, __o: Union[str, TextWithTTS]) -> TextWithTTS:
        if isinstance(__o, TextWithTTS):
            return TextWithTTS(self.text + __o.text,
                               self.tts + __o.tts)
        return TextWithTTS(self.text + __o,
                           self.tts + __o)

    def __radd__(self, __o: Union[str, TextWithTTS]) -> TextWithTTS:
        if isinstance(__o, TextWithTTS):
            return TextWithTTS(__o.text + self.text,
                               __o.tts + self.tts)
        return TextWithTTS(__o + self.text,
                           __o + self.text)

    def __iadd__(self, __o: Union[str, TextWithTTS]) -> TextWithTTS:
        return self + __o

    def join(self, __iterable: Iterable[TextWithTTS], /):
        """Likewise str.join, concatenate any number of TextWithTTS.

        Calls str.join for text parts and tts parts of TextWithTTS objects
        seperately and returns a new instance with concatenated text and tts.
        TextWithTTS whose method is being called inserts its text and tts
        between the concatenated objects.

        Args:
            Iterable[TextWithTTS]: sequence of TextWithTTS to concatenate

        Returns:
            TextWithTTS: the concatenation result
        """

        return TextWithTTS(self.text.join(map(lambda x: x.text, __iterable)),
                           self.tts.join(map(lambda x: x.tts, __iterable)))


class IdComparable:
    _id: Any

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, self.__class__) and self._id == __o._id


def gentle_capitalize(text: str):
    """Make the first character of a string have upper case
    leaving the rest of the string as is, unlike built-in
    str.capitalize method, which makes all other characters
    have lower case.

    Args:
        text (str): the string to convert

    Returns:
        str: gently capitalized string
    """

    if not text:
        return text
    return text[0].upper() + text[1:]


def construct_random_message(*parts: List[TextWithTTS], insert_spaces=True):
    """Construct randomly generated message from a sequence
    of message parts options.

    Args:
        *parts (List[TextWithTTS]): message parts options
        in the sequential order.

        insert_spaces (bool, optional): whether to insert
        spaces inbetween the parts of a message or not.
        Degaults to True.

    Returns:
        TextWithTTS: constructed message
    """
    return TextWithTTS(" " if insert_spaces else "").join(
        map(lambda x: random.choice(x),
            parts))
