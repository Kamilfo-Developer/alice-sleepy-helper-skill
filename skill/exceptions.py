class IncorrectConditionError(Exception):
    """Raised when an incorrect condition passed to a Repo method"""

    pass


class NoSuchEntityInDB(Exception):
    """Raised by a Repo when no passed entity found in the DB"""

    pass
