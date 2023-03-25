class IncorrectConditionError(Exception):
    """raises when an incorrect condition passed to a Repo method"""

    pass


class InvalidInputError(Exception):
    """raises when an incorrect input passed to skill methods"""

    pass
