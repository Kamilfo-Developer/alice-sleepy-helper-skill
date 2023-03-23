from typing import List, Any
import datetime
import random
from skill.utils import TextWithTTS, Daytime, gentle_capitalize
from skill.utils import construct_random_message
from skill.messages.unicode_literals import DASH
from skill.messages.base_messages import BaseMessages


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
        replicas_a = [
            TextWithTTS("Вы находитесь в главном меню."),
            TextWithTTS("Это главное меню Сонного Помощника."),
            TextWithTTS("Вы в главном меню."),
            TextWithTTS("Вы находитесь в главном меню Сонного Помощника"),
        ]

        replicas_b = [
            TextWithTTS("Здесь вам доступны все функции навыка."),
            TextWithTTS("Чем я могу помочь?"),
            TextWithTTS("Чем могу быть полезен?"),
            # TODO:                         ^^ Assure gender consistency
            TextWithTTS("Я к вашим услугам."),
            TextWithTTS("Что угодно, лишь бы вы спали хорошо."),
            # NOTE:      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Informal
        ]

        twtts = construct_random_message(replicas_a, replicas_b)

        return twtts

    def get_info_message(self) -> TextWithTTS:
        replicas_a = [
            TextWithTTS(
                f"Я {DASH} Сонный Помощник."
                " Я могу помочь вам со сном."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник. Я помогаю вам организовать"
                " свой сон."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник. Моя цель {DASH} помочь вам"
                " обеспечить себе правильный здоровый сон."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник. Моя цель {DASH} помочь вам"
                " обеспечить себе хороший и комфортный сон."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник, я могу помочь вам спать"
                " лучше и комфортнее."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник, я могу помочь вам"
                " высыпаться."
            ),
        ]

        replicas_b = [
            TextWithTTS(
                "Вы можете попросить меня рассчитать оптимальное для "
                "вас время сна, за которое вы можете выспаться"
            ),
            TextWithTTS(
                "Я могу рассчитать для вас оптимальное "
                "время сна, за которое вы можете выспаться"
            ),
            TextWithTTS(
                "С помощью меня, вы можете узнать, во сколько "
                "вам стоит сегодня лечь, чтобы выспаться"
            ),
            TextWithTTS(
                "Я могу помочь вам подобрать подходящее для вас "
                "время сна, чтобы вы смогли выспаться"
            ),
        ]

        replicas_c = [
            TextWithTTS(
                ". А ещё вы можете попросить у меня совет по тому, "
                "как лучше спать."
            ),
            TextWithTTS(
                ", или вы можете попросить у меня совет по тому, "
                "как лучше спать."
            ),
            TextWithTTS(
                ". А ещё я могу поделиться советом по здоровому сну."
            ),
            TextWithTTS(
                ", а ещё я могу дать вам небольшой совет по "
                "интересующему вас виду сна."
            ),
            TextWithTTS(
                ". Ещё я могу дать вам пару советов по улучшению "
                "качества вашего сна."
            ),
        ]

        twtts = construct_random_message(replicas_a, replicas_b, replicas_c)

        return twtts

    def get_ask_tip_topic_message(self) -> TextWithTTS:
        return TextWithTTS(text="Вас интересует совет по дневному или ночному сну?")

    def get_tip_message(self, tip: Any) -> TextWithTTS:
        return TextWithTTS(gentle_capitalize(tip.text),
                           gentle_capitalize(tip.tts))

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
        replicas = [
            TextWithTTS(text="Хорошего сна!"),
            TextWithTTS(text="Спокойной ночи!"),
            TextWithTTS(text="Доброй ночи!"),
            TextWithTTS(text="Сладких снов!"),
            TextWithTTS(text="Споки!"),
            # NOTE:           ^^^^^ Cringe
            TextWithTTS(text="Хороших вам сноведений!"),
            TextWithTTS(text="Крепкого сна!"),
            TextWithTTS(text="Отбой!"),
            # NOTE:           ^^^^^ Informal
        ]
        return random.choice(replicas)
