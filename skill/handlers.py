import datetime
import logging

from aioalice import Dispatcher
from aioalice.dispatcher import MemoryStorage
from aioalice.types import Button
from aioalice.types.alice_request import AliceRequest
from pytz import timezone

from skill.db.repos.sa_repo import SARepo
from skill.db.sa_db_settings import sa_repo_config
from skill.messages.ru_messages import RUMessages
from skill.sleep_calculator import SleepMode
from skill.states import States
from skill.user_manager import UserManager

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)

dp = Dispatcher(storage=MemoryStorage())

ICO_ID = "1540737/a491c8169a8b2597ba37"


def get_buttons_with_text(texts: list[str] | None) -> list[Button] | None:
    if texts is None:
        return None
    result = []
    for text in texts:
        button = Button(title=text)  # type: ignore
        result.append(button)

    return result


def contains_intent(req: AliceRequest, intent_name: str) -> bool:
    return intent_name in req.request._raw_kwargs["nlu"].get("intents")


@dp.request_handler(
    state=States.all(),  # type: ignore
    func=lambda req: contains_intent(req, "QUIT_SKILL"),
)
async def quit_skill(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_quit_message()
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        end_session=True,
    )


@dp.request_handler(
    state=States.all(),  # type: ignore
    func=lambda req: contains_intent(req, "TO_MENU"),
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


@dp.request_handler(
    state=States.all(),  # type: ignore
    func=lambda req: contains_intent(req, "YANDEX.HELP"),
)
async def ask_help(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_help_message()
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(
    state=States.MAIN_MENU,
    func=lambda req: contains_intent(req, "GIVE_INFO"),
)  # type: ignore
async def give_info(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_info_message()
    return alice_request.response_big_image(
        text=text_with_tts.text,
        image_id=ICO_ID,
        title="О навыке",
        description=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )


@dp.request_handler(
    state=States.MAIN_MENU,
    func=lambda req: contains_intent(req, "GIVE_WHAT_CAN_YOU_DO"),
)  # type: ignore
async def give_info(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_what_can_you_do_message()
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )


@dp.request_handler(
    state=States.ASKING_FOR_TIP,
    func=lambda req: contains_intent(req, "WANT_NIGHT_TIP"),  # type: ignore
)
async def send_night_tip(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_tip("ночной")
    await dp.storage.set_state(user_id, response.state)
    text_with_tts = response.text_with_tts
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(response.buttons_text),
    )


@dp.request_handler(
    state=States.ASKING_FOR_TIP,
    func=lambda req: contains_intent(req, "WANT_DAY_TIP"),
)  # type: ignore
async def send_day_tip(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_tip("дневной")
    await dp.storage.set_state(user_id, response.state)
    text_with_tts = response.text_with_tts
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(response.buttons_text),
    )


@dp.request_handler(state=States.ASKING_FOR_TIP)  # type: ignore
async def reask_tip_topic(alice_request: AliceRequest):
    text_with_tts = RUMessages().get_wrong_topic_message("")
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(
    func=lambda req: contains_intent(req, "ASK_FOR_TIP"),  # type: ignore
)
async def send_tip(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    text_with_tts = RUMessages().get_ask_tip_topic_message()
    await dp.storage.set_state(user_id, States.ASKING_FOR_TIP)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(
            RUMessages.TIP_TOPIC_SELECTION_BUTTONS_TEXT
        ),
    )


@dp.request_handler(
    state=States.IN_CALCULATOR,
    func=lambda req: contains_intent(req, "SHORT_SLEEP"),  # type: ignore
)
async def choose_short_duration(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    user_timezone = timezone(alice_request.meta.timezone)
    hour = time["hour"]
    minute = time.get("minute")
    if minute is None:
        minute = 0
    wake_up_time = (
        datetime.datetime.now(user_timezone)
        .time()
        .replace(hour=hour, minute=minute, tzinfo=user_timezone)
    )
    user_manager = await UserManager.new_manager(
        user_id=user_id, repo=SARepo(sa_repo_config), messages=RUMessages()
    )
    response = await user_manager.ask_sleep_time(
        now=datetime.datetime.now(timezone(alice_request.meta.timezone)),
        wake_up_time=wake_up_time,
        mode=SleepMode.SHORT,
    )
    text_with_tts = response.text_with_tts
    await dp.storage.set_state(user_id, States.CALCULATED)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(response.buttons_text),
    )


@dp.request_handler(
    state=States.IN_CALCULATOR,
    func=lambda req: contains_intent(req, "LONG_SLEEP"),  # type: ignore
)
async def choose_long_duration(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    # time when user wants to get up, saved from previous dialogues
    time = await dp.storage.get_data(user_id)
    user_timezone = timezone(alice_request.meta.timezone)
    hour = time["hour"]
    minute = time.get("minute")
    if minute is None:
        minute = 0
    wake_up_time = (
        datetime.datetime.now(user_timezone)
        .time()
        .replace(hour=hour, minute=minute, tzinfo=user_timezone)
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
        buttons=get_buttons_with_text(response.buttons_text),
    )


@dp.request_handler(state=States.SELECTING_TIME)  # type: ignore
async def enter_calculator(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    if "nlu" not in alice_request.request._raw_kwargs.keys():
        response = RUMessages().get_ask_wake_up_time_message().text
        return response
    try:
        value = alice_request.request._raw_kwargs["nlu"]["intents"][
            "sleep_calc"
        ]["slots"]["time"]["value"]
    except KeyError:
        text_with_tts = RUMessages().get_wrong_time_message()
        return alice_request.response(
            response_or_text=text_with_tts.text,
            tts=text_with_tts.tts,
        )
    if "hour" not in value.keys():
        text_with_tts = RUMessages().get_wrong_time_message()
        return alice_request.response(
            response_or_text=text_with_tts.text,
            tts=text_with_tts.tts,
        )
    if "minute" not in value.keys():
        value["minutes"] = 0
    # save time sleep time
    await dp.storage.set_data(user_id, value)
    text_with_tts = RUMessages().get_ask_sleep_mode_message()
    await dp.storage.set_state(user_id, States.IN_CALCULATOR)
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(
            RUMessages.SLEEP_MODE_SELECTION_BUTTONS_TEXT
        ),
    )


dp.register_request_handler(
    enter_calculator,
    state=States.MAIN_MENU,  # type: ignore
    func=lambda req: contains_intent(req, "MAIN_FUNCTIONALITY_ENTER_FAST"),
)


@dp.request_handler(
    state=States.MAIN_MENU,
    func=lambda req: contains_intent(req, "MAIN_FUNCTIONALITY_ENTER"),  # type: ignore
)
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
        buttons=get_buttons_with_text(response.buttons_text),
    )


@dp.request_handler(
    state=States.TIME_PROPOSED,
    func=lambda req: contains_intent(req, "YANDEX.REJECT"),
)  # type: ignore
async def enter_calculator_new_time(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    text_with_tts = RUMessages().get_ask_wake_up_time_message()
    await dp.storage.set_state(user_id, States.SELECTING_TIME)
    return alice_request.response(
        response_or_text=text_with_tts.text, tts=text_with_tts.tts
    )


@dp.request_handler(
    state=States.TIME_PROPOSED,
    func=lambda req: contains_intent(req, "YANDEX.CONFIRM"),
)  # type: ignore
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
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(
            RUMessages.SLEEP_MODE_SELECTION_BUTTONS_TEXT
        ),
    )


@dp.request_handler(
    state=States.CALCULATED,
    func=lambda req: contains_intent(req, "YANDEX.REJECT"),
)  # type: ignore
async def end_skill(alice_request: AliceRequest):
    user_id = alice_request.session.user_id
    await dp.storage.set_state(user_id, States.MAIN_MENU)
    text_with_tts = RUMessages().get_good_night_message()
    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages().MENU_BUTTONS_TEXT),
    )


dp.register_request_handler(
    send_night_tip,
    state=States.CALCULATED,  # type: ignore
    func=lambda req: contains_intent(req, "YANDEX.CONFIRM"),
)


@dp.request_handler()
async def welcome_user(alice_request: AliceRequest):
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
        buttons=get_buttons_with_text(response.buttons_text),
    )


@dp.errors_handler()
async def error_handler(alice_request: AliceRequest, e):
    user_id = alice_request.session.user_id
    state = await dp.storage.get_state(user_id)
    logging.error(str(state), exc_info=e)
    text_with_tts = RUMessages().get_generic_error_message()

    await dp.storage.set_state(user_id, States.MAIN_MENU)

    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages().MENU_BUTTONS_TEXT),
    )


@dp.request_handler(
    state=States.all(),  # type: ignore
)
async def universal_handler(alice_request: AliceRequest):
    user_id = alice_request.session.user_id

    text_with_tts = RUMessages().get_menu_welcome_message()

    await dp.storage.set_state(user_id, States.MAIN_MENU)

    return alice_request.response(
        response_or_text=text_with_tts.text,
        tts=text_with_tts.tts,
        buttons=get_buttons_with_text(RUMessages.MENU_BUTTONS_TEXT),
    )
