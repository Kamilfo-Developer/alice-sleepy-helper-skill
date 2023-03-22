class TextWithTTS:
    text: str
    tts: str

    def __init__(self, text: str, tts: str):
        self.text = text
        self.tts = tts
