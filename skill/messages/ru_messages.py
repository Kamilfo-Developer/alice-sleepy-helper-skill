from skill.messages.base_messages import BaseMessages
import datetime
from skill.utils import TextWithTTS, Daytime, gentle_capitalize
from skill.messages.unicode_literals import DASH
from typing import List, Any


class RUMessages(BaseMessages):
    def __init__(self):
        pass

    def get_start_message_intro(self, time: datetime.datetime) -> TextWithTTS:
        daytime = Daytime.from_time(time)
        greeting_text = ""
        match daytime:
            case Daytime.DAY:
                greeting_text = "Добрый день!"
            case Daytime.MORNING:
                greeting_text = "Доброе утро!"
            case Daytime.EVENING:
                greeting_text = "Добрый вечер!"
            case Daytime.NIGHT:
                greeting_text = "Доброй ночи!"

        twtts = TextWithTTS(
            text=f"{greeting_text} Я {DASH} Сонный Помощник, я помогаю вам"
            " организовать свой сон."
        )
        return twtts

    def get_start_message_comeback(
        self, time: datetime.datetime, streak: int, scoreboard: int
    ) -> TextWithTTS:
        daytime = Daytime.from_time(time)
        greeting_text = ""
        match daytime:
            case Daytime.DAY:
                greeting_text = "Добрый день!"
            case Daytime.MORNING:
                greeting_text = "Доброе утро!"
            case Daytime.EVENING:
                greeting_text = "Добрый вечер!"
            case Daytime.NIGHT:
                greeting_text = "Доброй ночи!"

        twtts = TextWithTTS(
            text=f"{greeting_text} "
            f"Сегодня вы пользуетесь Сонным Помощником {streak} день "
            f"подряд. Так держать! Вы спите лучше, чем {scoreboard}%"
            " пользователей!"
        )
        return twtts

    def get_menu_welcome_message(self) -> TextWithTTS:
        return TextWithTTS(
            text="Вы находитесь в главном меню. "
            "Здесь вам доступны все функции Сонного Помощника."
        )

    def get_info_message(self) -> TextWithTTS:
        return TextWithTTS(
            text=f"Я {DASH} Сонный Помощник, я могу помочь вам организовать"
            " свой здоровый сон. Вы можете попросить меня рассчитать"
            " оптимальное для вас время сна, за которое вы можете"
            " выспаться. А ещё вы можете попросить у меня совет по"
            " тому, как лучше спать."
        )

    def get_ask_tip_topic_message(self) -> TextWithTTS:
        return TextWithTTS(text="Вас интересует совет по дневному или ночному сну?")

    def get_tip_message(self, tip: Any) -> TextWithTTS:
        return TextWithTTS(gentle_capitalize(tip.text), gentle_capitalize(tip.tts))

    def get_propose_yesterday_wake_up_time_message(
        self, last_time: datetime.time
    ) -> TextWithTTS:
        return TextWithTTS(
            text="Вы хотите завтра встать как в прошлый раз,"
            f" в {last_time.isoformat(timespec='minutes')}?"
        )

    def get_ask_wake_up_time_message(self) -> TextWithTTS:
        return TextWithTTS(text="Во сколько вы хотите завтра проснуться?")

    def get_ask_sleep_mode_message(self) -> TextWithTTS:
        return TextWithTTS(text="Выберите режим сна.")

    def get_sleep_calc_time_message(
        self, bed_time: datetime.time, activities: List[Any]
    ) -> TextWithTTS:
        text = "Хорошо, рекомендую вам лечь в "
        text += f"{bed_time.isoformat(timespec='minutes')}. "
        tts = text
        if activities:
            text += "За этот вечер вы можете успеть, например, "
            tts = text
            activities_text = [act.description for act in activities]
            activities_tts = [act.tts for act in activities]
            if len(activities) > 1:
                activities_text[-1] = " или ".join(
                    (activities_text[-2], activities_text[-1])
                )
                activities_tts[-1] = " или ".join(
                    (activities_tts[-2], activities_tts[-1])
                )
            text += ", ".join(activities_text) + ". "
            tts += ", ".join(activities_tts) + ". "

        text += "Не желаете-ли получить совет по сну?"
        tts += "Не желаете-ли получить совет по сну?"

        return TextWithTTS(text=text, tts=tts)

    def get_good_night_message(self) -> TextWithTTS:
        return TextWithTTS(text="Хорошего сна!")
