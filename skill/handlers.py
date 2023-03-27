from aioalice import Dispatcher
from aioalice.dispatcher import MemoryStorage
from skill.messages.ru_messages import RUMessages
from skill.sleep_calculator import SleepMode
from skill.user_manager import UserManager
from skill.db.repos.sa_repo import SARepo
from skill.db.sa_db_settings import sa_repo_config
from skill.states import States
import datetime

dp = Dispatcher(storage=MemoryStorage())

# Key words for:
# Escaping to main menu
TO_MENU_REPLICS = ["выйди", "меню"]
# Asking info
GIVE_INFO_REPLICS = ["расскажи о навыке", "что ты делаешь"]
# Asking tip
ASK_FOR_TIP_REPLICS = ["посоветуй"]
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
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_tip("Night")
    response = response.text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.ASKING_FOR_TIP, contains=WANT_DAY_TIP)
async def send_day_tip(alice_request):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_tip("Day")
    response = response.text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.MAIN_MENU, contains=ASK_FOR_TIP_REPLICS)
async def send_tip(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_ask_tip_topic_message().text
    await dp.storage.set_state(user_id, SkillStates.ASKING_FOR_TIP)
    return alice_request.response(response)


@dp.request_handler(
    state=SkillStates.IN_CALCULATOR, contains=SHORT_SLEEP_KEYWORDS
)
async def choose_short_duration(alice_request):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    wake_up_time = (
        datetime.datetime.now()
        .replace(hour=time["hour"], minute=time["minute"])
        .time()
    )
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_sleep_time(
        now=datetime.datetime.now(),
        wake_up_time=wake_up_time,
        mode=SleepMode.LONG,
    )
    response = response.text
    await dp.storage.set_state(user_id, SkillStates.CALCULATED)
    return alice_request.response(response)


@dp.request_handler(
    state=SkillStates.IN_CALCULATOR, contains=LONG_SLEEP_KEYWORDS
)
async def choose_long_duration(alice_request):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    wake_up_time = (
        datetime.datetime.now()
        .replace(hour=time["hour"], minute=time["minute"])
        .time()
    )
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_sleep_time(
        now=datetime.datetime.now(),
        wake_up_time=wake_up_time,
        mode=SleepMode.LONG,
    )
    response = response.text
    await dp.storage.set_state(user_id, SkillStates.CALCULATED)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.SELECTING_TIME)
async def enter_calculator(alice_request):
    user_id = alice_request.session.user_id
    value = alice_request.request._raw_kwargs["nlu"]["intents"]["sleep_calc"][
        "slots"
    ]["time"]["value"]
    # save time sleep time
    await dp.storage.set_data(user_id, value)
    response = RUMessages().get_ask_sleep_mode_message().text
    await dp.storage.set_state(user_id, SkillStates.IN_CALCULATOR)
    return alice_request.response(response)


dp.register_request_handler(
    enter_calculator,
    state=SkillStates.MAIN_MENU,
    contains=MAIN_FUNCTIONALITY_ENTER_FAST,
)


@dp.request_handler(
    state=SkillStates.MAIN_MENU, contains=MAIN_FUNCTIONALITY_ENTER
)
async def enter_calculator_with_no_time(alice_request):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    last_wake_up_time = user_manager.user.last_wake_up_time
    if last_wake_up_time is not None:
        response = (
            RUMessages()
            .get_propose_yesterday_wake_up_time_message(last_wake_up_time)
            .text
        )
        await dp.storage.set_state(user_id, SkillStates.TIME_PROPOSED)
        return alice_request.response(response)
    response = RUMessages().get_ask_wake_up_time_message().text
    await dp.storage.set_state(user_id, SkillStates.SELECTING_TIME)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.TIME_PROPOSED, contains=NO_REPLICS)
async def enter_calculator_new_time(alice_request):
    user_id = alice_request.session.user_id
    response = RUMessages().get_ask_wake_up_time_message().text
    await dp.storage.set_state(user_id, SkillStates.SELECTING_TIME)
    return alice_request.response(response)


@dp.request_handler(state=SkillStates.TIME_PROPOSED, contains=YES_REPLICS)
async def enter_calculator_proposed_time(alice_request):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    time = {
        "hour": user_manager.user.last_wake_up_time.hour,
        "minute": user_manager.user.last_wake_up_time.minute,
    }
    await dp.storage.set_data(user_id, time)
    response = RUMessages().get_ask_sleep_mode_message().text
    await dp.storage.set_state(user_id, SkillStates.IN_CALCULATOR)
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
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.check_in(now=datetime.datetime.now())
    response = response.text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)


@dp.request_handler()
async def welcome_old_user(alice_request):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.check_in(now=datetime.datetime.now())
    response = response.text
    await dp.storage.set_state(user_id, SkillStates.MAIN_MENU)
    return alice_request.response(response)
