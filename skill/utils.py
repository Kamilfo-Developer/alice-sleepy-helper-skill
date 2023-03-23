from typing import Any


class TextWithTTS:
    text: str
    tts: str

    def __init__(self, text: str, tts: str):
        self.text = text
        self.tts = tts

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, TextWithTTS)
            and self.text == __o.text
            and self.tts == __o.tts
        )

    def __str__(self) -> str:
        return "Text:\n" f"{self.text}" "\n" "TTS:\n" f"{self.tts}"


class IdComparable:
    _id: Any

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, self.__class__) and self._id == __o._id
