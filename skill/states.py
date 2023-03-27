from aioalice.utils.helper import Helper, HelperMode, Item


class States(Helper):
    mode = HelperMode.snake_case

    MAIN_MENU = Item()  # = main_menu
    ASKING_FOR_TIP = Item()  # = asking_for_tip
    SELECTING_TIME = Item()  # = selecting_time
    IN_CALCULATOR = Item()  # = in_calculator
    CALCULATED = Item()  # = calculated
    TIME_PROPOSED = Item()  # = time_proposed
