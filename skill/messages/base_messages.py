import abc
import datetime

from skill.utils import TextWithTTS
from typing import List
from skill.sleep_calculator import SleepCalculation
from skill.entities import Tip, Activity

from typing import Any, List



class BaseMessages(abc.ABC):
    MENU_BUTTONS_TEXT: list[str]
    TIP_TOPIC_SELECTION_BUTTONS_TEXT: list[str]
    SLEEP_TIME_PROPOSAL_BUTTONS_TEXT: list[str]
    SLEEP_MODE_SELECTION_BUTTONS_TEXT: list[str]
    POST_SLEEP_CALCULATION_BUTTONS_TEXT: list[str]

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_start_message_intro(self, time: datetime.datetime) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_start_message_comeback(
        self, time: datetime.datetime, streak: int, scoreboard: int
    ) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_menu_welcome_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_info_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_ask_tip_topic_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_propose_yesterday_wake_up_time_message(
        self, last_time: datetime.time
    ) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_ask_wake_up_time_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_ask_sleep_mode_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_tip_message(self, tip: Tip) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_sleep_calc_time_message(
        self,
        sleep_calc_result: SleepCalculation,
        activities: List[Activity],
    ) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_good_night_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_wrong_topic_message(self, topic_name: str) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_generic_error_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_wrong_time_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_help_message(self) -> TextWithTTS:
        pass

    @abc.abstractmethod
    def get_quit_message(self) -> TextWithTTS:
        pass
