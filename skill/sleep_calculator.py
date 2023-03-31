import enum
import datetime
from skill.exceptions import InvalidInputError
from typing import Iterable
from skill.entities import Activity


class SleepMode(enum.Enum):
    LONG = enum.auto()
    SHORT = enum.auto()
    VERY_LONG = enum.auto()
    VERY_SHORT = enum.auto()


class SleepCalculator:
    @staticmethod
    def activities_compilation(
        time_a: datetime.datetime,
        time_b: datetime.datetime,
        all_activities: Iterable[Activity],
        limit: int = 2,
    ) -> list[Activity]:
        """Returns a number of activities that can be done between time_a and
        time_b.

        Args:
            time_a (datetime.datetime): opening time boundary

            time_b (datetime.datetime): closing time boundary

            all_activities (Iterable[Activity]): the pool of all activities

            limit (int, optional): the number of best fitting activities to
            return.
            Defaults to 2

        Returns:
            list[Activity]: the list of best fitting activities compilation
        """

        if time_b < time_a:
            raise InvalidInputError(
                "Closing boundary cannot be less than the opening boundary"
            )
        delta = time_b - time_a
        sorted_activities = sorted(
            filter(lambda x: x.occupation_time < delta, all_activities),
            reverse=True,
            key=lambda x: x.occupation_time,
        )
        return sorted_activities[:limit]

    @staticmethod
    def calc(
        wake_up_time: datetime.datetime,
        origin_time: datetime.datetime | None = None,
        mode: SleepMode = SleepMode.LONG,
    ) -> datetime.datetime:
        """Returns the time at which the user need to go to bed according to
        their request.

        Args:
            wake_up_time (datetime.datetime): user's desired time to wake up

            origin_time (datetime.datetime | None, optional): the starting
            point in time from which the calculations are made.
            If None is passed, origin_time sets to datetime.datetime.now()
            result with the timezone of wake_up_time.
            Defaults to None

            mode (SleepMode.SHORT | Sleepmode.LONG | Sleepmode.VERY_SHORT | Sleepmode.VERY_LONG): user's desired sleep mode

        Returns:
            datetime.datetime: the time at which the user should go to bed
        """

        if origin_time is None:
            origin_time = datetime.datetime.now(wake_up_time.tzinfo)
            # Adds time to prepare for sleep
            origin_time += datetime.timedelta(minutes=20) 

        if wake_up_time <= origin_time:
            raise InvalidInputError(
                "Wake up time is earlier than current time"
            )
        
        if mode == SleepMode.SHORT:
            step = datetime.timedelta(minutes=15)
            delta = wake_up_time - origin_time
            delta_steps = delta // step
            sleep_time = delta_steps * step
            # Sets the maximum possible sleep time to be 4:30
            max_time = datetime.timedelta(hours=4, minutes=30)
            sleep_time = min(sleep_time, max_time)
            return wake_up_time - sleep_time

        if mode == SleepMode.LONG:
            step = datetime.timedelta(hours=1, minutes=30)
            delta = wake_up_time - origin_time
            delta_steps = delta // step
            sleep_time = delta_steps * step
            # Sets the maximum possible sleep time to be 9:00
            max_time = datetime.timedelta(hours=9, minutes=0)
            sleep_time = min(sleep_time, max_time)
            return wake_up_time - sleep_time

        raise InvalidInputError(f"Invalid sleep mode given: {mode}")
