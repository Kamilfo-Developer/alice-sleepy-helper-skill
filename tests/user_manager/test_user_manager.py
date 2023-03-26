from pytz import timezone
from tests.sa_db_settings import sa_repo_config
from skill.db.repos.sa_repo import SARepo
from skill.entities import User, Activity, TipsTopic
from skill.user_manager import UserManager
from skill.messages.ru_messages import RUMessages
from skill.sleep_calculator import SleepMode
from skill.utils import TextWithTTS
import pytest
import datetime
import random
from uuid import uuid4


def generate_random_string_id() -> str:
    return "".join(
        (random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"))
        for x in range(64)
    )


@pytest.mark.asyncio
async def test_check_in():
    repo = SARepo(sa_repo_config)
    messages = RUMessages()
    now = datetime.datetime.now(datetime.UTC)

    for user in await repo.get_users():
        await repo.delete_user(user)

    test_user_id = generate_random_string_id()

    loser_user = User(
        id=generate_random_string_id(),
        streak=0,
        last_skill_use=(now - datetime.timedelta(days=1)),
        last_wake_up_time=datetime.time(hour=4, minute=20),
        heard_tips=[],
        join_date=datetime.datetime(year=2022, month=1, day=1),
        repo=repo,
    )

    user = User(
        id=test_user_id,
        streak=4,
        last_skill_use=(now - datetime.timedelta(days=1)),
        last_wake_up_time=datetime.time(hour=4, minute=20),
        heard_tips=[],
        join_date=datetime.datetime(year=2022, month=1, day=1),
        repo=repo,
    )
    await repo.insert_users((user, loser_user))

    user_manager = await UserManager.new_manager(
        test_user_id, repo, messages, create_user_if_not_found=False
    )

    assert user_manager is not None

    message = await user_manager.check_in(now)

    assert "5 день подряд" in message.text  # type: ignore
    assert "50%" in message.text  # type: ignore

    user_upd = await repo.get_user_by_id(test_user_id)

    assert bool(user_upd)

    assert user_upd._streak == 5
    assert user_upd.last_skill_use == now

    # Fast forward 5 days later
    now = now + datetime.timedelta(days=5)
    user_manager = await UserManager.new_manager(
        test_user_id, repo, messages, create_user_if_not_found=False
    )

    assert bool(user_manager)

    message = await user_manager.check_in(now)

    assert "день подряд" not in message.text  # type: ignore

    user_upd = await repo.get_user_by_id(test_user_id)

    assert bool(user_upd)
    assert user_upd._streak == 0
    assert user_upd.last_skill_use == now


@pytest.mark.asyncio
async def test_sleep_calc():
    repo = SARepo(sa_repo_config)
    messages = RUMessages()

    test_user_id = generate_random_string_id()
    user_manager = await UserManager.new_manager(test_user_id, repo, messages)
    user_test = await repo.get_user_by_id(test_user_id)

    assert bool(user_test) and bool(user_manager)

    assert user_manager.is_new_user()

    message1 = await user_manager.get_ask_sleep_time_message()

    assert "как в прошлый раз" not in message1.text

    now = datetime.datetime(
        year=1420, month=1, day=1, hour=1, minute=0, second=0
    )

    wake_up_time = datetime.time(hour=14, minute=0, second=0)

    message2 = await user_manager.ask_sleep_time(
        now, wake_up_time, SleepMode.LONG
    )

    assert not user_manager.is_new_user()

    assert "02:00" in message2.text  # type: ignore

    message2 = await user_manager.ask_sleep_time(
        now, wake_up_time, SleepMode.SHORT
    )

    assert "12:30" in message2.text  # type: ignore

    message3 = await user_manager.get_ask_sleep_time_message()

    assert "14:00" in message3.text


@pytest.mark.asyncio
async def test_activities_proposal():
    repo = SARepo(sa_repo_config)
    messages = RUMessages()

    test_user_id = generate_random_string_id()
    user_manager = await UserManager.new_manager(test_user_id, repo, messages)
    user_test = await repo.get_user_by_id(test_user_id)

    assert bool(user_test) and bool(user_manager)

    now = datetime.datetime(
        year=1420,
        month=1,
        day=1,
        hour=11,
        minute=00,
        second=0,
        tzinfo=datetime.UTC,
    )

    for activity in await repo.get_activities():
        await repo.delete_activity(activity)

    activity1 = Activity(
        id=uuid4(),
        description=TextWithTTS("[FINDME_1] моргнуть"),
        created_date=now,
        occupation_time=datetime.timedelta(hours=0, minutes=0, seconds=1),
        repo=repo,
    )
    activity2 = Activity(
        id=uuid4(),
        description=TextWithTTS("[FINDME_2] анжуманя"),
        created_date=now,
        occupation_time=datetime.timedelta(hours=1, minutes=29, seconds=1),
        repo=repo,
    )
    activity3 = Activity(
        id=uuid4(),
        description=TextWithTTS("[EXCLUDEME] бегит"),
        created_date=now,
        occupation_time=datetime.timedelta(hours=2, minutes=29, seconds=1),
        repo=repo,
    )

    await repo.insert_activities((activity1, activity2, activity3))

    wake_up_time = datetime.time(hour=14, minute=0, second=0)

    message1 = await user_manager.ask_sleep_time(
        now, wake_up_time, SleepMode.SHORT
    )

    assert message1.text.count("[FINDME_1]") == 1  # type: ignore
    assert message1.text.count("[FINDME_2]") == 1  # type: ignore
    assert message1.text.count("[EXCLUDEME]") == 0  # type: ignore

    now = datetime.datetime(
        year=1420, month=1, day=1, hour=12, minute=30, second=0
    )

    message2 = await user_manager.ask_sleep_time(
        now, wake_up_time, SleepMode.SHORT
    )

    assert message2.text.count("[FINDME_1]") == 0  # type: ignore
    assert message2.text.count("[FINDME_2]") == 0  # type: ignore
    assert message2.text.count("[EXCLUDEME]") == 0  # type: ignore


@pytest.mark.asyncio
async def test_tips():
    repo = SARepo(sa_repo_config)
    messages = RUMessages()

    test_user_id = generate_random_string_id()
    user_manager = await UserManager.new_manager(test_user_id, repo, messages)
    assert bool(user_manager)

    for tip in await repo.get_tips():
        await repo.delete_tip(tip)

    now = datetime.datetime.now()

    tips_topic = TipsTopic(
        id=uuid4(),
        name=TextWithTTS("как правильно мыть руки"),
        topic_description=TextWithTTS("вот как"),
        created_date=now,
        repo=repo,
    )

    await repo.insert_tips_topic(tips_topic)

    await tips_topic.add_tip(
        short_description=TextWithTTS("святая вода"),
        tip_content=TextWithTTS("[1] мойте руки святой водой кншн"),
        tips_topic=tips_topic,
        created_date=now,
    )
    await tips_topic.add_tip(
        short_description=TextWithTTS("зачем"),
        tip_content=TextWithTTS("[2] не мойте руки вообще никак вы что дурак"),
        tips_topic=tips_topic,
        created_date=now,
    )
    await tips_topic.add_tip(
        short_description=TextWithTTS("оближи"),
        tip_content=TextWithTTS("[3] всё что нам нужно у нас в руках"),
        tips_topic=tips_topic,
        created_date=now,
    )

    for _ in range(10):
        user = await repo.update_user(user_manager.user.drop_heard_tips())
        user_manager = UserManager(user, repo, messages)

        message1 = await user_manager.ask_tip(tips_topic._id)
        assert isinstance(message1, TextWithTTS)
        exclude = False
        for tag in ("[1]", "[2]", "[3]"):
            if tag in message1.text:
                exclude = tag
                break
        assert exclude
        message2 = await user_manager.ask_tip(tips_topic._id)
        assert isinstance(message2, TextWithTTS)
        assert exclude not in message2.text
