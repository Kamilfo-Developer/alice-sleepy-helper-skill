from __future__ import annotations

import datetime
import logging
import random
from dataclasses import dataclass
import pytz
from skill.entities import User
from skill.exceptions import InvalidInputError
from skill.db.repos.base_repo import BaseRepo
from skill.messages.base_messages import BaseMessages
from skill.sleep_calculator import SleepCalculator, SleepMode
from skill.states import States
from skill.utils import TextWithTTS


@dataclass
class SkillResponse:
    text_with_tts: TextWithTTS
    state: str | None
    buttons_text: list[str] | None


class UserManager:
    user: User
    repo: BaseRepo
    messages: BaseMessages

    def __init__(
        self, user: User, repo: BaseRepo, messages: BaseMessages
    ) -> None:
        self.user = user
        self.repo = repo
        self.messages = messages

    @classmethod
    async def new_manager(
        cls,
        user_id: str,
        repo: BaseRepo,
        messages: BaseMessages,
        create_user_if_not_found: bool = True,
    ) -> UserManager:
        """Sets up UserManager with given user repo and messages.
        If user_id is not found in the DB and create_user_if_not_found
        is True, creates a new user.

        Args:
            user_id (str): User's ID as it is stored in the DB
            and returned in the API request

            repo (BaseRepo): the repo which this user manager should
            work with

            messages (BaseMessages): the messages generator used
            by reply constructors

            create_user_if_not_found (bool, optional): whether to create
            a new user if user_id is not found in the DB or not.
            Defaults to True.

        Returns:
            UserManager | None: proper UserManager instance. If
            the user_id is not found in the DB and create_user_if_not_found
            is False, returns None
        """

        user = await repo.get_user_by_id(user_id)
        # if not user and not create_user_if_not_found:
        #    return None

        if not user:
            user = User(
                id=user_id,
                streak=0,
                last_skill_use=None,
                last_wake_up_time=None,
                heard_tips=[],
                join_date=datetime.datetime.now(),
                repo=repo,
            )
            await repo.insert_user(user)

        inst = cls(user=user, repo=repo, messages=messages)
        return inst

    def is_new_user(self):
        return not (self.user.last_skill_use or self.user.last_wake_up_time)

    async def count_scoreboard(self, percentages: bool = True) -> int:
        """Calculates user's position in the global streak scoreboard,
        starting from the lowest.

        Args:
            percentages (bool, optional): whether to convert the score
            to percentage rate of users with lower streak or not
            Defaults to True

        Returns:
            int: user's scoreboard position or the percentage rate
        """

        streak = self.user._streak

        score = await self.repo.count_users_with_streak(streak, "<=") - 1
        if not percentages:
            return score
        total = await self.repo.count_all_users()
        percentage = round(score / total * 100)
        return percentage

    async def check_in(
        self, now: datetime.datetime | None = None
    ) -> SkillResponse:
        """Perform all needed processes when a user starts the skill.
        To be more precise, this method:
        - Drops user's streak if the streak is lost
        - Increases user's streak if the streak is kept
        - Updates user's last_skill_use field

        Returns a properly constructed greeting message to welcome the user

        Args:
            now (datetime.datetime | None, optional): the time at which the
            user started the skill. If not set, the method will recieve the
            time with datetime.datetime.now() (using UTC). However, leaving
            this parameter to None is deprecated due to the possible difference
            between the request time and the execution time.
            Defaults to None.

        Returns:
            TextWithTTS: a greeting message.
        """
        if now is None:
            now = datetime.datetime.now(pytz.utc)

        new_user = True

        if self.user.last_skill_use is not None:
            new_user = False
            yesterday = (now - datetime.timedelta(days=1)).date()
            today = now.date()
            if self.user.last_skill_use.date() == yesterday:
                # Last skill use was yesterday, streak increased
                self.user.increase_streak()
            elif self.user.last_skill_use.date() != today:
                # Last skill use was neither yesterday, nor today,
                # thus streak dropped.
                self.user.drop_streak()

        self.user.last_skill_use = now

        await self.repo.update_user(self.user)

        if new_user:
            return SkillResponse(
                self.messages.get_start_message_intro(now),
                States.MAIN_MENU,
                self.messages.MENU_BUTTONS_TEXT,
            )
        streak = self.user._streak

        scoreboard = await self.count_scoreboard(percentages=True)
        return SkillResponse(
            self.messages.get_start_message_comeback(
                time=now, streak=streak, scoreboard=scoreboard
            ),
            States.MAIN_MENU,
            self.messages.MENU_BUTTONS_TEXT,
        )

    async def ask_tip(self, topic_name: str) -> SkillResponse:
        """Chooses a tip on given topic that has most likely never
        been heard before by the user and tracks the heard tips buffer.

        Args:
            topic_name (str): the name of the topic of tips

        Returns:
            TextWithTTS: a tip message in a form of TextWithTTS or
            error message if the topic is not found.
        """

        topic = await self.repo.get_tips_topic_by_name(topic_name)
        if topic is None:
            return SkillResponse(
                self.messages.get_wrong_topic_message(topic_name),
                States.ASKING_FOR_TIP,
                self.messages.TIP_TOPIC_SELECTION_BUTTONS_TEXT,
            )
        tips = await self.repo.get_topic_tips(topic_id=topic._id)
        heard_tips = self.user._heard_tips

        if len(heard_tips) == len(tips):
            self.user.drop_heard_tips()
            heard_tips = []

        if heard_tips:
            tips = list(filter(lambda x: x not in heard_tips, tips))

        tip = random.choice(tips)

        self.user.add_heard_tip(tip)

        await self.repo.update_user(self.user)
        return SkillResponse(
            self.messages.get_tip_message(tip),
            States.MAIN_MENU,
            self.messages.MENU_BUTTONS_TEXT,
        )

    async def get_ask_sleep_time_message(self) -> SkillResponse:
        """Get the proper message to ask a user the time at which
        they want to wake up. The selected message depends on whether
        the user have already used the sleep calculator or not."""

        last_wake_up_time = self.user.last_wake_up_time
        if last_wake_up_time is not None:
            return SkillResponse(
                self.messages.get_propose_yesterday_wake_up_time_message(
                    last_wake_up_time
                ),
                States.TIME_PROPOSED,
                self.messages.SLEEP_TIME_PROPOSAL_BUTTONS_TEXT,
            )
        return SkillResponse(
            self.messages.get_ask_wake_up_time_message(),
            States.SELECTING_TIME,
            None,
        )

    async def ask_sleep_time(
        self,
        now: datetime.datetime,
        wake_up_time: datetime.time,
        mode: SleepMode,
        remember_time: bool = True,
    ) -> SkillResponse:
        """Calculate user's sleep time. Constructs a response message,
        in which it proposes the user a number of activities for the rest of
        the evening, and returns the message.

        Args:
            now (datetime.datetime): the timestamp at which the user asks to
            calculate their sleep time.

            wake_up_time (datetime.time): the time at which the user
            wants to wake up

            mode (SleepMode.LONG | SleepMode.SHORT): user's selected
            sleep mode

            remember_time (bool, optional): whether to record the time at which
            the user wants to wake up to the DB or not
            Defaults to True.

        Returns:
            TextWithTTS: a response message in a form of TextWithTTS.
        """
        logging.debug(wake_up_time)
        if remember_time:
            self.user.last_wake_up_time = wake_up_time
            await self.repo.update_user(self.user)

        try:
            wake_up_datetime = datetime.datetime.combine(
                date=now.date(),
                time=wake_up_time,
                tzinfo=now.tzinfo,
            )
            sleep_calc_result = SleepCalculator.calc(
                wake_up_time=wake_up_datetime, origin_time=now, mode=mode
            )
        except InvalidInputError:
            wake_up_datetime = datetime.datetime.combine(
                date=(now + datetime.timedelta(days=1)).date(),
                time=wake_up_time,
                tzinfo=now.tzinfo,
            )
            sleep_calc_result = SleepCalculator.calc(
                wake_up_time=wake_up_datetime, origin_time=now, mode=mode
            )
        all_activities = await self.repo.get_activities()
        activities = SleepCalculator.activities_compilation(
            now, sleep_calc_result.bed_time, all_activities
        )
        return SkillResponse(
            self.messages.get_sleep_calc_time_message(
                sleep_calc_result, activities
            ),
            States.CALCULATED,
            self.messages.POST_SLEEP_CALCULATION_BUTTONS_TEXT,
        )
