from ru_messages import RUMessages

POSIX_alliases = {
    'ru-RU': RUMessages
}


def auto(locale):
    """Determine what Messages class should be used according to
    user's locale.

    Args:
        locale (str): POSIX language code

    Returns:
        Type[BaseMessages]: Messages class for the specified language

    """

    if locale not in POSIX_alliases:
        return RUMessages
    return POSIX_alliases[locale]
