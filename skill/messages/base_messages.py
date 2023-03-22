import abc
from .context_flags import Daytime


class BaseMessages(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_start_message_intro(self, time: Daytime):
        pass

    @abc.abstractmethod
    def get_start_message_comeback(self, time: Daytime):
        pass


