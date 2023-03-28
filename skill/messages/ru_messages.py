from __future__ import annotations
from typing import List, TYPE_CHECKING
import datetime
import random
from skill.utils import TextWithTTS, Daytime, gentle_capitalize
from skill.utils import construct_random_message
from skill.messages.unicode_literals import DASH, LAQUO, RAQUO
from skill.messages.base_messages import BaseMessages

if TYPE_CHECKING:
    from skill.entities import Tip, Activity


class RUMessages(BaseMessages):
    MENU_BUTTONS_TEXT = [
        "Дай совет",
        "Рассчитай сон",
        "Расскажи о навыке",
    ]
    TIP_TOPIC_SELECTION_BUTTONS_TEXT = ["Дневной сон", "Ночной сон"]
    SLEEP_TIME_PROPOSAL_BUTTONS_TEXT = ["Да", "Нет"]
    SLEEP_MODE_SELECTION_BUTTONS_TEXT = ["Короткий", "Длинный"]
    POST_SLEEP_CALCULATION_BUTTONS_TEXT = ["Да", "Нет"]

    def __init__(self):
        pass

    def get_start_message_intro(self, time: datetime.datetime) -> TextWithTTS:
        daytime = Daytime.from_time(time)
        greeting = TextWithTTS("Здравствуйте!")
        match daytime:
            case Daytime.DAY:
                greeting = TextWithTTS("Добрый день!")
            case Daytime.MORNING:
                greeting = TextWithTTS("Доброе утро!")
            case Daytime.EVENING:
                greeting = TextWithTTS("Добрый вечер!")
            case Daytime.NIGHT:
                greeting = TextWithTTS("Доброй ночи!")

        intro = TextWithTTS(
            f"Я {DASH} Сонный Помощник. Я помогаю вам организовать" " ваш сон."
        )

        man = TextWithTTS(
            "Вы можете попросить меня рассчитать оптимальное для "
            "вас время сна, за которое вы можете выспаться. "
            f"Для этого скажите {LAQUO}Я хочу спать{RAQUO}. "
            "А ещё вы можете попросить меня дать вам пару "
            "советов по тому, как лучше высыпаться."
        )

        replicas_tail = [
            TextWithTTS("Чем я могу помочь?"),
            TextWithTTS("Чем могу помочь?"),
            TextWithTTS("Чем могу быть полезен?"),
            # TODO:                         ^^ Assure gender consistency
            TextWithTTS("Я к вашим услугам."),
        ]

        message = TextWithTTS(" ").join(
            (greeting, intro, man, random.choice(replicas_tail))
        )

        return message

    def get_start_message_comeback(
        self, time: datetime.datetime, streak: int, scoreboard: int
    ) -> TextWithTTS:
        daytime = Daytime.from_time(time)
        greeting = TextWithTTS("Здравствуйте! ")
        match daytime:
            case Daytime.DAY:
                greeting = TextWithTTS("Добрый день! ")
            case Daytime.MORNING:
                greeting = TextWithTTS("Доброе утро! ")
            case Daytime.EVENING:
                greeting = TextWithTTS("Добрый вечер! ")
            case Daytime.NIGHT:
                greeting = TextWithTTS("Доброй ночи! ")

        message = greeting

        if streak > 1:
            praise = TextWithTTS(
                f"Сегодня вы пользуетесь Сонным Помощником {streak}"
                " день подряд. "
            )
            replicas_insert = [
                TextWithTTS("Так держать!"),
                TextWithTTS("Замечательно!"),
                TextWithTTS("Здорово!"),
                TextWithTTS("Ура!"),
                TextWithTTS("Прекрасно!"),
                TextWithTTS("Продолжайте в том же духе!"),
            ]
            praise += random.choice(replicas_insert)
            praise += TextWithTTS(
                f" Вы спите лучше, чем {scoreboard}% пользователей! "
            )

            message += praise

        replicas_tail = [
            TextWithTTS("Чем я могу помочь?"),
            TextWithTTS("Чем могу помочь?"),
            TextWithTTS("Чем могу быть полезен?"),
            # TODO:                         ^^ Assure gender consistency
            TextWithTTS("Я к вашим услугам."),
        ]

        message += random.choice(replicas_tail)

        return message

    def get_menu_welcome_message(self) -> TextWithTTS:
        replicas_a = [
            TextWithTTS("Вы находитесь в главном меню."),
            TextWithTTS("Это главное меню Сонного Помощника."),
            TextWithTTS("Вы в главном меню."),
            TextWithTTS("Вы находитесь в главном меню Сонного Помощника."),
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

        message = construct_random_message(replicas_a, replicas_b)

        return message

    def get_info_message(self) -> TextWithTTS:
        replicas_a = [
            TextWithTTS(
                f"Я {DASH} Сонный Помощник."
                " Я могу помочь людям, испытывающим проблемы со сном."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник. Я помогаю людям, которые хотят"
                " организовать свой сон."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник. Моя цель {DASH} помочь"
                " обеспечить себе правильный здоровый сон тем, кому этого не хватало."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник. Моя цель {DASH} помочь"
                " невыспавшимся людям обеспечить "
                " себе хороший комфортный сон."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник, я могу помочь лучше спать тем,"
                " кто испытывает с этим проблемы."
            ),
            TextWithTTS(
                f"Я {DASH} Сонный Помощник, я могу помочь вам высыпаться,"
                " если у вас есть проблемы со сном."
            ),
        ]

        replicas_b = [
            TextWithTTS(
                "Вы можете попросить меня рассчитать оптимальное для "
                "вас время сна, за которое вы можете выспаться."
            ),
            TextWithTTS(
                "Я могу рассчитать для вас оптимальное "
                "время сна, за которое вы можете выспаться."
            ),
            TextWithTTS(
                "С помощью меня, вы можете узнать, во сколько "
                "вам стоит сегодня лечь, чтобы выспаться."
            ),
            TextWithTTS(
                "Я могу помочь вам подобрать подходящее для вас "
                "время сна, чтобы вы смогли выспаться."
            ),
        ]

        replicas_c = [
            TextWithTTS(f"Для этого скажите {LAQUO}Я хочу спать{RAQUO}."),
            TextWithTTS(
                "Чтобы вызвать эту функцию, скажитe "
                f"{LAQUO}Я хочу спать{RAQUO}."
            ),
        ]

        replicas_d = [
            TextWithTTS(
                "А ещё вы можете попросить у меня совет по тому, "
                "как лучше спать."
            ),
            TextWithTTS(
                "Или вы можете попросить у меня совет по тому, "
                "как лучше спать."
            ),
            TextWithTTS("А ещё я могу поделиться советом по здоровому сну."),
            TextWithTTS(
                "А ещё я могу дать вам небольшой совет по "
                "интересующему вас виду сна."
            ),
            TextWithTTS(
                "Ещё я могу дать вам пару советов по улучшению "
                "качества вашего сна."
            ),
            TextWithTTS(
                "А ещё я могу дать вам пару советов по тому, "
                "как высыпаться."
            ),
        ]

        message = construct_random_message(
            replicas_a, replicas_b, replicas_c, replicas_d
        )

        return message

    def get_ask_tip_topic_message(self) -> TextWithTTS:
        replicas = [
            TextWithTTS("Вас интересует совет по дневному или ночному сну?"),
            TextWithTTS(
                "По какому сну вы хотите получить совет, дневному, "
                "или ночному? "
            ),
            TextWithTTS(
                "Я могу дать вам совет по дневному или ночному сну. "
                "Какой сон вас интересует?"
            ),
            TextWithTTS(
                "С каким сном вам нужна помощь? С дневным или ночным?"
            ),
            TextWithTTS("Вам нужна помощь по дневному или ночному сну?"),
        ]
        # NOTE: Tip topic options are currently hardcoded.
        #       This may cause issues if new tip topics
        #       are planned to be added in the future.
        return random.choice(replicas)

    def get_tip_message(self, tip: Tip) -> TextWithTTS:
        return tip.tip_content.transform(gentle_capitalize)

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
        replicas = [
            TextWithTTS(
                "Как много вы хотите спать? Выберите "
                "один из режимов сна: короткий или длинный сон"
            ),
            TextWithTTS("Вас интересует длинный или короткий сон?"),
            TextWithTTS(
                "Какой режим сна вы бы предпочли, длинный или короткий?"
            ),
        ]
        return random.choice(replicas)

    def get_sleep_calc_time_message(
        self, bed_time: datetime.time, activities: List[Activity]
    ) -> TextWithTTS:

        message = TextWithTTS(
            "Хорошо, рекомендую вам лечь в "
            f"{bed_time.isoformat(timespec='minutes')}. "
        )
        if activities:
            message += TextWithTTS(
                "За этот вечер вы можете успеть, например, "
            )

            activities_text_with_tts = [act.description for act in activities]
            if len(activities) > 1:
                # Construct activity enumerating statement in proper Russian
                # syntax: objects are seperated by a comma and a whitespace
                # except for the last two, which have the word "или" inbetween.
                activities_text_with_tts[-1] = TextWithTTS(" или ").join(
                    (
                        activities_text_with_tts[-2],
                        activities_text_with_tts[-1],
                    )
                )  # Glue the last two objects together with the word "или"
                activities_text_with_tts.pop(-2)  # Get rid of the penultimate
                #                                   object duplicate

            message += TextWithTTS(", ").join(activities_text_with_tts) + ". "

        replica_tail = [
            TextWithTTS("Не желаете-ли получить совет по сну?"),
            TextWithTTS("Не хотите-ли получить совет по сну?"),
            TextWithTTS("Хотите получить совет по сну?"),
            TextWithTTS("Как насчёт совета по сну?"),
            TextWithTTS("Как насчёт небольшого совета по сну?"),
            TextWithTTS("Вас интересует совет по сну?"),
            TextWithTTS("Хотите совет по сну?"),
        ]
        message += random.choice(replica_tail)

        return message

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

    def get_wrong_topic_message(self, topic_name: str) -> TextWithTTS:
        return TextWithTTS(
            "Пожалуйста, выберите один из вариантов тем для совета: "
            " дневной сон или ночной сон, или вернитесь в главное меню, сказав"
            f" {LAQUO}Меню{RAQUO}"
        )
        # TODO: Rephrase replica and add variety

    def get_generic_error_message(self) -> TextWithTTS:
        return TextWithTTS("Что-то пошло не так, вы были возвращены в меню.")

    def get_wrong_time_message(self) -> TextWithTTS:
        return TextWithTTS(
            "Пожалуйста, укажите корректное время, или вернитесь в главное "
            f"меню, сказав {LAQUO}Меню{RAQUO}"
        )
    
    def get_help_message(self) -> TextWithTTS:
        return TextWithTTS(
            f"Cкажите {LAQUO}Меню{RAQUO}, чтобы перейти в главное меню\n"
            f"Скажите {LAQUO}Я хочу спать{RAQUO}, чтобы рассчитать оптимальное время сна\n"
            f"Скажите {LAQUO}Дай ссовет{RAQUO}, чтобы получить совет по сну\n"
            f"Скажите {LAQUO}Расскажи о навыке{RAQUO}, чтобы узнать побольше о навыке\n"
        )
