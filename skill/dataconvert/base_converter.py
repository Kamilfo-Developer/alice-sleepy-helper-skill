import abc
import datetime


class BaseDataConverter(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def time(obj: dict, timezone: str) -> datetime.time:
        ...

    @staticmethod
    @abc.abstractmethod
    def datetime(obj: dict, timezone: str) -> datetime.datetime:
        ...
