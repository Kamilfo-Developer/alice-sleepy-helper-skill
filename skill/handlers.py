from aioalice import Dispatcher
from aioalice.dispatcher import MemoryStorage
from aioalice.types.alice_request import AliceRequest
from aioalice.types import Button
from skill.messages.ru_messages import RUMessages
from skill.sleep_calculator import SleepMode
from skill.user_manager import UserManager
from skill.db.repos.sa_repo import SARepo
from skill.db.sa_db_settings import sa_repo_config
from skill.states import States
from pytz import timezone
import datetime
import logging

logging.basicConfig(format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

dp = Dispatcher(storage=MemoryStorage())

# Key words for:
# Escaping to main menu
TO_MENU_REPLICS = ["выйди", "меню", "Меню"]
# Asking info
GIVE_INFO_REPLICS = ["расскажи о навыке", "что ты делаешь", "что ты умеешь"]
# Asking tip
ASK_FOR_TIP_REPLICS = ["посоветуй", "совет", "лайфхак", "подскажи", "подсказка"]
# Using main functionality (sleep time calculation)
MAIN_FUNCTIONALITY_ENTER = ["я хочу спать"]
# Using main functionality (sleep time calculation) (skip asking the time)
MAIN_FUNCTIONALITY_ENTER_FAST = ["Во сколько", "Когда", "Через сколько"]
# Choosing short sleep mode
SHORT_SLEEP_KEYWORDS = ["маленький", "короткий", "недолгий", "небольшой"]
# Choosing long sleep mode
LONG_SLEEP_KEYWORDS = ["большой", "длинный", "долгий"]
# Yes answer
YES_REPLICS = ["да", "конечно", "естественно", "хочу"]
# No answer
NO_REPLICS = ["нет", "отказываюсь", "не хочу"]
# Asking tip about night sleep
WANT_NIGHT_TIP = ["ночной"]
# Asking tip abot day slip
WANT_DAY_TIP = ["дневной"]


def get_buttons_with_text(texts: list[str]) -> list[Button]:
    result = []
    for text in texts:
        button = Button(title=text)
        result.append(button)

    return result


@dp.request_handler(state=States.MAIN_MENU, contains=GIVE_INFO_REPLICS)
async def give_info(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_info_message()
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )


@dp.request_handler(state=States.ASKING_FOR_TIP, contains=WANT_NIGHT_TIP)
async def send_night_tip(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_tip("Ночной сон")
    await dp.storage.set_state(user_id, response.state)
    text_with_tts = response.text_with_tts
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(state=States.ASKING_FOR_TIP, contains=WANT_DAY_TIP)
async def send_day_tip(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_tip("Дневной сон")
    await dp.storage.set_state(user_id, response.state)
    text_with_tts = response.text_with_tts
    if response.state == States.ASKING_FOR_TIP
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(state=States.ASKING_FOR_TIP)
async def reask_tip_topic(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_wrong_topic_message("")
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(state=States.MAIN_MENU, contains=ASK_FOR_TIP_REPLICS)
async def send_tip(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    text_with_tts = RUMessages().get_ask_tip_topic_message()
    await dp.storage.set_state(user_id, States.ASKING_FOR_TIP)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.TIP_TOPIC_SELECTION_BUTTONS_TEXT),
    )


@dp.request_handler(state=States.IN_CALCULATOR, contains=SHORT_SLEEP_KEYWORDS)
async def choose_short_duration(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    wake_up_time = (
        datetime.datetime.now(timezone(alice_request.meta.timezone))
        .replace(hour=time["hour"], minute=time["minute"])
        .time()
    )
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_sleep_time(
        now=datetime.datetime.now(timezone(alice_request.meta.timezone)),
        wake_up_time=wake_up_time,
        mode=SleepMode.LONG,
    )
    text_with_tts = response.text_with_tts
    await dp.storage.set_state(user_id, States.CALCULATED)
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(state=States.IN_CALCULATOR, contains=LONG_SLEEP_KEYWORDS)
async def choose_long_duration(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    wake_up_time = (
        datetime.datetime.now(timezone(alice_request.meta.timezone))
        .replace(hour=time["hour"], minute=time["minute"])
        .time()
    )
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_sleep_time(
        now=datetime.datetime.now(timezone(alice_request.meta.timezone)),
        wake_up_time=wake_up_time,
        mode=SleepMode.LONG,
    )
    text_with_tts = response.text_with_tts
    await dp.storage.set_state(user_id, States.CALCULATED)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.POST_SLEEP_CALCULATION_BUTTONS_TEXT),
    )


@dp.request_handler(state=States.SELECTING_TIME)
async def enter_calculator(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    if "nlu" not in alice_request.request._raw_kwargs.keys():
        response = RUMessages().get_ask_wake_up_time_message().text
        return response
    value = alice_request.request._raw_kwargs["nlu"]["intents"]["sleep_calc"]["slots"][
        "time"
    ]["value"]
    # save time sleep time
    await dp.storage.set_data(user_id, value)
    text_with_tts = RUMessages().get_ask_sleep_mode_message()
    await dp.storage.set_state(user_id, States.IN_CALCULATOR)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.SLEEP_MODE_SELECTION_BUTTONS_TEXT),
    )


dp.register_request_handler(
    enter_calculator,
    state=States.MAIN_MENU,
    contains=MAIN_FUNCTIONALITY_ENTER_FAST,
)


@dp.request_handler(state=States.MAIN_MENU, contains=MAIN_FUNCTIONALITY_ENTER)
async def enter_calculator_with_no_time(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.get_ask_sleep_time_message()
    await dp.storage.set_state(user_id, response.state)
    text_with_tts = response.text_with_tts
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.SLEEP_TIME_PROPOSAL_BUTTONS_TEXT),
    )


@dp.request_handler(state=States.TIME_PROPOSED, contains=NO_REPLICS)
async def enter_calculator_new_time(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    text_with_tts = RUMessages().get_ask_wake_up_time_message()
    await dp.storage.set_state(user_id, States.SELECTING_TIME)
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(state=States.TIME_PROPOSED, contains=YES_REPLICS)
async def enter_calculator_proposed_time(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    time = {
        "hour": user_manager.user.last_wake_up_time.hour,
        "minute": user_manager.user.last_wake_up_time.minute,
    }
    await dp.storage.set_data(user_id, time)
    text_with_tts = RUMessages().get_ask_sleep_mode_message()
    await dp.storage.set_state(user_id, States.IN_CALCULATOR)
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(state=States.CALCULATED, contains=NO_REPLICS)
async def end_skill(alice_request: AliceRequest):
    # It must end skill
    text_with_tts = RUMessages().get_good_night_message()
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts, end_session=True
    )


dp.register_request_handler(
    send_night_tip, state=States.CALCULATED, contains=YES_REPLICS
)


@dp.request_handler()
async def welcome_old_user(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.check_in(
        now=datetime.datetime.now(timezone(alice_request.meta.timezone))
    )
    text_with_tts = response.text_with_tts
    await dp.storage.set_state(user_id, States.MAIN_MENU)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )

'''
@dp.errors_handler()
async def error_handler(alice_request: AliceRequest, e):
    user_id = alice_request.session.user_id
    state = await dp.storage.get_state(user_id)
    logging.error(str(state))
    text_with_tts = RUMessages().get_menu_welcome_message()

    await dp.storage.set_state(user_id, States.MAIN_MENU)

    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )
'''

@dp.request_handler(
    state=[
        States.IN_CALCULATOR,
        States.ASKING_FOR_TIP,
        States.CALCULATED,
        States.MAIN_MENU,
        States.SELECTING_TIME,
        States.TIME_PROPOSED,
    ],
    # contains=TO_MENU_REPLICS,
)
async def go_to_menu(alice_request: AliceRequest):
    user_id = alice_request.session.user_id

    text_with_tts = RUMessages().get_menu_welcome_message()

    await dp.storage.set_state(user_id, States.MAIN_MENU)

    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )
