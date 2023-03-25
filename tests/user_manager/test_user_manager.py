from tests.user_manager.sa_db_settings import sa_repo_config
from skill.db.repos.sa_repo import SARepo
from skill.entities import User
from skill.user_manager import UserManager
from skill.messages.ru_messages import RUMessages
import pytest
import datetime


@pytest.mark.asyncio
async def test_check_in():
    repo = SARepo(sa_repo_config)
    messages = RUMessages()
    now = datetime.datetime.now()

    test_user_id = "testid_1"

    user = User(
        id="testid_1",
        streak=4,
        last_skill_use=(
            now - datetime.timedelta(days=1)
        ),
        last_wake_up_time=datetime.time(hour=4, minute=20),
        heard_tips=[],
        join_date=datetime.datetime(year=2022, month=1, day=1),
        repo=repo
    )
    await repo.insert_user(user)

    user_manager = await UserManager.new_manager(
        test_user_id, repo, messages, create_user_if_not_found=False
    )

    assert user_manager is not None

    print(await user_manager.check_in(now))

    user_upd = await repo.get_user_by_id(test_user_id)

    assert bool(user_upd)

    assert user_upd._streak == 5
    assert user.last_skill_use == now

    # Fast forward 5 days later
    now += datetime.timedelta(days=5)

    print(await user_manager.check_in(now))
    user_upd = await repo.get_user_by_id(test_user_id)

    assert bool(user_upd)
    assert user_upd._streak == 0
    assert user.last_skill_use == now

# TODO: Add tests for tip handling, get_sleep_time_message and sleep
#       calculation (with activities)
