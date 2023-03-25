from __future__ import annotations
import datetime
import random
from uuid import UUID
from skill.entities import User, Tip
from skill.db.repos.base_repo import BaseRepo
from skill.messages.base_messages import BaseMessages
from skill.utils import TextWithTTS
from skill.sleep_calculator import SleepCalculator, SleepMode


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
        cls, user_id: str, repo: BaseRepo, messages: BaseMessages
    ) -> UserManager | None:
        """Sets up UserManager with given user repo and messages.

        Args:
            user_id (str): User's ID as it is stored in the DB
            and returned in the API request

            repo (BaseRepo): the repo which this user manager should
            work with

            messages (BaseMessages): the messages generator used
            by reply constructors

        Returns:
            UserManager | None: proper UserManager instance. If
            the user is not found in the repo, returns None
        """
        user = await repo.get_user_by_id(user_id)
        if user is None:
            return None

        inst = cls(user=user, repo=repo, messages=messages)
        return inst

    async def count_scoreboard(self, percentages: bool = True) -> int:
        # TODO:^^^^^^^^^^^^^^^
        #      Potentially heavy function when dealing
        #      with a large number of users. Maybe the
        #      feature can be done with SQL queries? RFC
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

        users = map(lambda x: x._streak, await self.repo.get_users())

        scores = sorted(users)
        score = scores.index(streak)
        if not percentages:
            return score
        total = len(scores)
        percentage = round(score / total * 100)
        return percentage

    async def check_in(
        self, now: datetime.datetime | None = None, reply: bool = True
    ) -> TextWithTTS | None:
        """Perform all needed processes when a user starts the skill.
        To be more precise, this method:
        - Drops user's streak if the streak is lost
        - Increases user's streak if the streak is kept
        - Updates user's last_skill_use field

        If reply argument is set to True, this method constructs a greeting
        message and returns it.

        Args:
            now (datetime.datetime | None, optional): the time at which the
            user started the skill. If not set, the method will recieve the
            time with datetime.datetime.now(). However, leaving this
            parameter to None is deprecated due to the possible difference
            between the request time and the execution time.
            Defaults to None.

            reply (bool, optional): whether to return a greeting message or not
            Defaults to True.

        Returns:
            TextWithTTS | None: if reply is set to True, a greeting message.
            Otherwise None.
        """
        if now is None:
            now = datetime.datetime.now()

        new_user = False

        if self.user.last_skill_use is not None:
            new_user = True
            delta = now - self.user.last_skill_use
            borderline = datetime.timedelta(days=1)
            if delta > borderline:
                self.user.drop_streak()
            else:
                self.user.increase_streak()
        self.user.last_skill_use = now

        await self.repo.update_user(self.user)

        if not reply:
            return None

        if new_user:
            return self.messages.get_start_message_intro(now)
        streak = self.user._streak

        scoreboard = await self.count_scoreboard(percentages=True)
        return self.messages.get_start_message_comeback(
            time=now, streak=streak, scoreboard=scoreboard
        )

    async def ask_tip(
        self, topic_id: UUID, reply: bool = True
    ) -> TextWithTTS | Tip:
        """Chooses a tip on given topic that has most likely never
        been heard before by the user and tracks the heard tips buffer.
        If reply argument is set to True, this method constructs a tip
        message and returns it.

        Args:
            topic_id (UUID): the UUID of the topic of tips

            reply (bool, optional): whether to return a tip message or not
            Defaults to True.

        Returns:
            TextWithTTS | Tip: if reply is set to True, a tip message in
            a form of TextWithTTS. Otherwise the selected tip.
        """

        tips = await self.repo.get_topic_tips(topic_id=topic_id)
        heard_tips = self.user._heard_tips

        if len(heard_tips) == len(tips):
            self.user.drop_heard_tips()
            heard_tips = []

        if heard_tips:
            tips = list(filter(lambda x: x not in heard_tips, tips))

        tip = random.choice(tips)

        self.user.add_heard_tip(tip)

        await self.repo.update_user(self.user)

        if not reply:
            return tip
        return self.messages.get_tip_message(tip)

    async def ask_sleep_time(
        self,
        now: datetime.datetime,
        wake_up_time: datetime.time,
        mode: SleepMode,
        reply: bool = True,
    ) -> TextWithTTS | datetime.datetime:
        """Calculate user's sleep time. If reply argument is set to True,
        this method constructs a response message, in which it proposes the
        user a number of activities for the evening, and returns the message.

        Args:
            now (datetime.datetime): the timestamp at which the user asks to
            calculate their sleep time.

            wake_up_time (datetime.time): the time at which the user
            wants to wake up

            mode (SleepMode.LONG | SleepMode.SHORT): user's selected
            sleep mode

            reply (bool, optional): whether to return a response message or not
            Defaults to True.

        Returns:
            TextWithTTS | datetime.datetime: if reply is set to True, a
            response message in a form of TextWithTTS. Otherwise the proposed
            timestamp for a user to go to bed.
        """

        now_time = now.time()

        wake_up_datetime = datetime.datetime.combine(
            date=(
                (now + datetime.timedelta(days=1)).date()
                if wake_up_time < now_time
                else now.date()
            ),
            time=wake_up_time,
        )

        bed_time = SleepCalculator.calc(now, wake_up_datetime, mode)
        if not reply:
            return bed_time

        all_activities = await self.repo.get_activities()
        activities = SleepCalculator.activities_compilation(
            now, bed_time, all_activities
        )
        return self.messages.get_sleep_calc_time_message(
            bed_time.time(), activities
        )
