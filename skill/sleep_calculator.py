import enum
import datetime
from skill.sh_exceptions import SHInvalidInputError
from typing import Iterable
from skill.entities import Activity


class SleepMode(enum.Enum):
    LONG = enum.auto()
    SHORT = enum.auto()


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

        if time_b <= time_a:
            raise SHInvalidInputError(
                "Closing boundary cannot be less than the opening boundary"
            )
        delta = time_b - time_a
        matching_activities = filter(
            lambda x: x.occupation_time < delta, all_activities
        )
        sorted_activities = sorted(
            matching_activities, reverse=True, key=lambda x: x.occupation_time
        )
        return sorted_activities[:limit]

    @staticmethod
    def calc(
        origin_time: datetime.datetime | None,
        wake_up_time: datetime.datetime,
        mode: SleepMode = SleepMode.LONG,
    ) -> datetime.datetime:
        """Returns the time at which the user need to go to bed according to
        their request.

        Args:
            origin_time (datetime.datetime | None): the starting point in
            time from which the calculations are made.
            If None is passed, origin_time sets to datetime.datetime.now()
            result.

            wake_up_time (datetime.datetime): user's desired time to wake up

            mode (SleepMode.SHORT | Sleepmode.LONG): user's desired sleep mode

        Returns:
            datetime.datetime: the time at which the user should go to bed
        """

        if origin_time is None:
            origin_time = datetime.datetime.now()

        if wake_up_time <= origin_time:
            raise SHInvalidInputError(
                "Wake up time is earlier than current time"
            )

        step = datetime.timedelta(hours=1, minutes=30)

        if mode == SleepMode.SHORT:
            return wake_up_time - step

        if mode == SleepMode.LONG:
            delta = wake_up_time - origin_time
            delta_steps = delta // step
            return wake_up_time - ((delta_steps) * step)

        raise SHInvalidInputError(f"Invalid sleep mode given: {mode}")
