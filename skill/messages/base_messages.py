import abc


class BaseMessages(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_start_message(self, time):
        pass
