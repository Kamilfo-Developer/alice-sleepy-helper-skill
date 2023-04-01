import datetime

from skill.exceptions import InvalidInputError
from typing import Iterable, Callable
from skill.entities import Activity
from dataclasses import dataclass


class SleepModeDoesntFitError(Exception):
    pass

import enum
from typing import Iterable

from skill.entities import Activity
from skill.exceptions import InvalidInputError


class SleepMode(enum.Enum):
    LONG = enum.auto()
    MEDIUM = enum.auto()
    SHORT = enum.auto()
    VERY_SHORT = enum.auto()


@dataclass
class SleepCalculation:
    bed_time: datetime.datetime = datetime.datetime(datetime.MINYEAR, 1, 1)
    selected_mode: SleepMode = SleepMode.LONG
    sleep_time: datetime.timedelta = datetime.timedelta(0)
    changed_mode: SleepMode | None = None


class SleepCalculator:
    _mode_calculators: dict[
        SleepMode,
        Callable[[datetime.datetime, datetime.datetime], datetime.timedelta],
    ] = {}
    _mode_priorities: dict[
        SleepMode,
        int,
    ] = {}

    @classmethod
    def mode_calculator(cls, mode: SleepMode, priority: int):
        def wrapper(func):
            cls._mode_calculators[mode] = func
            cls._mode_priorities[mode] = priority

            def newfunc(*args, **kwargs):
                sleep_time = func(*args, **kwargs)
                if sleep_time <= datetime.timedelta(0):
                    raise SleepModeDoesntFitError(
                        "Can't fit any sleep time in given range"
                    )
                return sleep_time

            return newfunc

        return wrapper

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

    @classmethod
    def calc(
        cls,
        wake_up_time: datetime.datetime,
        origin_time: datetime.datetime | None = None,
        mode: SleepMode = SleepMode.LONG,
    ) -> SleepCalculation:
        """Returns the time at which the user need to go to bed according to
        their request.

        Args:
            wake_up_time (datetime.datetime): user's desired time to wake up

            origin_time (datetime.datetime | None, optional): the starting
            point in time from which the calculations are made.
            If None is passed, origin_time sets to datetime.datetime.now()
            result with the timezone of wake_up_time.
            Defaults to None

            mode (SleepMode.LONG | SleepMode.MEDIUM | SleepMode.SHORT |
            SleepMode.VERY_SHORT): user's desired sleep mode

        Returns:
            datetime.datetime: the time at which the user should go to bed
        """

        if origin_time is None:
            origin_time = datetime.datetime.now(wake_up_time.tzinfo)

        if wake_up_time <= origin_time:
            raise InvalidInputError(
                "Wake up time is earlier than current time"
            )

        result = SleepCalculation()
        result.selected_mode = mode

        # Initial calculation for the desired mode
        try:
            result.sleep_time = cls._mode_calculators[mode](
                origin_time, wake_up_time
            )
        except SleepModeDoesntFitError:
            # Impossible mode: choose the mode that fits the most
            sleep_time = None
            for mode, calculator in sorted(
                cls._mode_calculators.items(),
                key=lambda pair: cls._mode_priorities[pair[0]],
            ):
                try:
                    sleep_time = calculator(origin_time, wake_up_time)
                except SleepModeDoesntFitError:
                    continue
                result.sleep_time = sleep_time
                result.changed_mode = mode
                break

            if sleep_time is None:
                raise InvalidInputError(
                    "It is not possible to sleep in given period of time"
                )
        result.bed_time = wake_up_time - result.sleep_time
        return result


# TODO: Change the sleep mode definition architecture to be more
# developer-friendly (Issue #87)


@SleepCalculator.mode_calculator(SleepMode.VERY_SHORT, 3)
def vert_short_sleep(
    origin_time: datetime.datetime, wake_up_time: datetime.datetime
) -> datetime.timedelta:
    origin_time += datetime.timedelta(minutes=10)
    step = datetime.timedelta(hours=0, minutes=15)
    delta = wake_up_time - origin_time
    delta_steps = delta // step
    sleep_time = delta_steps * step
    min_time = datetime.timedelta(hours=0, minutes=15)
    max_time = datetime.timedelta(hours=3, minutes=0)
    sleep_time = min(sleep_time, max_time)
    if sleep_time < min_time:
        raise SleepModeDoesntFitError
    return sleep_time


@SleepCalculator.mode_calculator(SleepMode.SHORT, 2)
def short_sleep(
    origin_time: datetime.datetime, wake_up_time: datetime.datetime
) -> datetime.timedelta:
    origin_time += datetime.timedelta(minutes=20)
    step = datetime.timedelta(hours=1, minutes=00)
    delta = wake_up_time - origin_time
    delta_steps = delta // step
    sleep_time = delta_steps * step
    min_time = datetime.timedelta(hours=3, minutes=0)
    max_time = datetime.timedelta(hours=6, minutes=0)
    sleep_time = min(sleep_time, max_time)
    if sleep_time < min_time:
        raise SleepModeDoesntFitError
    return sleep_time


@SleepCalculator.mode_calculator(SleepMode.MEDIUM, 1)
def medium_sleep(
    origin_time: datetime.datetime, wake_up_time: datetime.datetime
) -> datetime.timedelta:
    origin_time += datetime.timedelta(minutes=20)
    step = datetime.timedelta(hours=1, minutes=30)
    delta = wake_up_time - origin_time
    delta_steps = delta // step
    sleep_time = delta_steps * step
    min_time = datetime.timedelta(hours=6, minutes=0)
    max_time = datetime.timedelta(hours=9, minutes=0)
    sleep_time = min(sleep_time, max_time)
    if sleep_time < min_time:
        raise SleepModeDoesntFitError
    return sleep_time


@SleepCalculator.mode_calculator(SleepMode.LONG, 0)
def long_sleep(
    origin_time: datetime.datetime, wake_up_time: datetime.datetime
) -> datetime.timedelta:
    origin_time += datetime.timedelta(minutes=20)
    step = datetime.timedelta(hours=1, minutes=30)
    delta = wake_up_time - origin_time
    delta_steps = delta // step
    sleep_time = delta_steps * step
    min_time = datetime.timedelta(hours=9, minutes=0)
    max_time = datetime.timedelta(hours=12, minutes=0)
    sleep_time = min(sleep_time, max_time)
    if sleep_time < min_time:
        raise SleepModeDoesntFitError
    return sleep_time
