from aioalice import Dispatcher
from aioalice.dispatcher import MemoryStorage
from aioalice.utils.helper import Helper, HelperMode, Item
from skill.messages.ru_messages import RUMessages
from skill.sleep_calculator import SleepCalculator, SleepMode
import datetime

dp = Dispatcher(storage=MemoryStorage())

# Списки ключевых слов для:
# выхода в главное меню
TO_MENU_REPLICS = ["выйди", "меню"]
# вызова информации
GIVE_INFO_REPLICS = ["расскажи о навыке", "что ты делаешь"]
# запроса совета
ASK_FOR_TIP_REPLICS = ["посоветуй"]
# входа в главную ветку сценария (рассчет времени отбоя)
MAIN_FUNCTIONALITY_ENTER = ["я хочу спать"]
# быстрый в ход в главную ветку
MAIN_FUNCTIONALITY_ENTER_FAST = ["Во сколько", "Когда", "Через сколько"]
# выбора короткого режима сна
SHORT_SLEEP_KEYWORDS = ["маленький", "короткий", "недолгий", "небольшой"]
# выбора длинного режима сна
LONG_SLEEP_KEYWORDS = ["большой", "длинный", "долгий"]
# ответа да
YES_REPLICS = ["да", "конечно", "естественно", "хочу"]
# ответа нет
NO_REPLICS = ["нет", "отказываюсь", "не хочу"]
# получения ночного совета
WANT_NIGHT_TIP = ["ночной"]
# получения дневного совета
WANT_DAY_TIP = ["дневной"]


class SkillStates(Helper):
    mode = HelperMode.snake_case

    MAIN_MENU = Item()  # = main_menu
    ASKING_FOR_TIP = Item()  # = asking_for_tip
    SELECTING_TIME = Item()  # = selecting_time
    IN_CALCULATOR = Item()  # = in_calculator
    CALCULATED = Item()  # = calculated


@dp.request_handler(contains=TO_MENU_REPLICS)
async def go_to_menu(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_menu_welcome_message().text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.MAIN_MENU, contains=GIVE_INFO_REPLICS)
async def give_info(alice_request):
    response = RUMessages().get_info_message().text
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.ASKING_FOR_TIP, contains=WANT_NIGHT_TIP)
async def send_night_tip(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_tip_message().text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.ASKING_FOR_TIP, contains=WANT_DAY_TIP)
async def send_day_tip(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_tip_message().text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.MAIN_MENU, contains=ASK_FOR_TIP_REPLICS)
async def send_tip(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_ask_tip_topic_message().text
    await dp.storage.set_state(user_id, SkillStates.ASKING_FOR_TIP)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.IN_CALCULATOR, contains=SHORT_SLEEP_KEYWORDS)
async def choose_short_duration(alice_request):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    wake_up_time = datetime.datetime.now().replace(
        hour=time["hour"], minute=time["minute"]
    )
    if datetime.datetime.now() > wake_up_time:
        wake_up_time = wake_up_time + datetime.timedelta(days=1)
    time_target = SleepCalculator.calc(
        now=datetime.datetime.now(), wake_up_time=wake_up_time, mode=SleepMode.SHORT
    )
    response = (
        RUMessages()
        .get_sleep_calc_time_message(bed_time=time_target, activities=[])
        .text
    )
    await dp.storage.set_state(user_id, SkillStates.CALCULATED)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.IN_CALCULATOR, contains=LONG_SLEEP_KEYWORDS)
async def choose_long_duration(alice_request):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    wake_up_time = datetime.datetime.now().replace(
        hour=time["hour"], minute=time["minute"]
    )
    if (
        datetime.datetime.now() > wake_up_time
    ):  # Если это время уже прошло, значит нам нужен завтрашний день
        wake_up_time = wake_up_time + datetime.timedelta(days=1)
    time_target = SleepCalculator.calc(
        now=datetime.datetime.now(), wake_up_time=wake_up_time, mode=SleepMode.LONG
    )
    response = (
        RUMessages()
        .get_sleep_calc_time_message(bed_time=time_target, activities=[])
        .text
    )
    await dp.storage.set_state(user_id, SkillStates.CALCULATED)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.SELECTING_TIME)
async def enter_calculator(alice_request):
    user_id = alice_request.session.user_id
    value = alice_request.request._raw_kwargs["nlu"]["intents"]["sleep_calc"]["slots"][
        "time"
    ]["value"]
    await dp.storage.set_data(user_id, value)
    response = RUMessages().get_ask_sleep_mode_message().text
    await dp.storage.set_state(user_id, SkillStates.IN_CALCULATOR)
    return alice_request.response(response)


dp.register_request_handler(
    enter_calculator,
    state=SkillStates.MAIN_MENU,
    contains=MAIN_FUNCTIONALITY_ENTER_FAST,
)


@dp.request_handler(state=SkillStates.MAIN_MENU, contains=MAIN_FUNCTIONALITY_ENTER)
async def enter_calculator_with_no_time(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_ask_wake_up_time_message().text
    await dp.storage.set_state(user_id, SkillStates.SELECTING_TIME)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.CALCULATED, contains=NO_REPLICS)
async def end_skill(alice_request):
    # It must end skill
    response = RUMessages().get_good_night_message().text
    return alice_request.response(response)


dp.register_request_handler(
    send_night_tip, state=SkillStates.CALCULATED, contains=YES_REPLICS
)


@dp.request_handler(func=lambda areq: areq.session.new)
async def welcome_user(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_start_message_intro(time=datetime.datetime.now()).text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler()
async def welcome_old_user(alice_request):
    user_id = alice_request.session.user_id
    response = (
        RUMessages().get_start_message_comeback(time=datetime.datetime.now()).text
    )
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)
