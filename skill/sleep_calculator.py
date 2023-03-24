import enum
import datetime
from skill.sh_exceptions import SHInvalidInput


class SleepMode(enum.Enum):
    LONG = enum.auto()
    SHORT = enum.auto()


class SleepCalculator:

    @staticmethod
    def calc(now: datetime.datetime, wake_up_time: datetime.datetime,
             mode: SleepMode = SleepMode.LONG) -> datetime.datetime:
        '''Returns the time at which the user need to go to bed according to
        their request.
        
        Args:
            now (datetime.datetime): current time
            wake_up_time (datetime.datetime): user's desired time to wake up
            mode (SleepMode.SHORT | Sleepmode.LONG): user's desired sleep mode
        
        Returns:
            datetime.datetime: the time at which the user should go to bed
        '''

        if wake_up_time <= now:
            raise SHInvalidInput("Wake up time is earlier than current time")

        step = datetime.timedelta(hours=1, minutes=30)

        if mode == SleepMode.SHORT:
            return wake_up_time - step
        
        if mode == SleepMode.LONG:
            delta = (wake_up_time - now)
            delta_steps = delta // step
            return wake_up_time - ((delta_steps) * step)
        
        raise SHInvalidInput(f"Invalid sleep mode given: {mode}")

