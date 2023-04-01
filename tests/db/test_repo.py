import random
from datetime import UTC, datetime, time, timedelta, timezone
from uuid import uuid4

import pytest
import pytest_asyncio

from skill.db.repos.base_repo import BaseRepo
from skill.db.repos.sa_repo import SARepo
from skill.entities import Activity, Tip, TipsTopic, User
from skill.exceptions import NoSuchEntityInDB
from skill.utils import TextWithTTS
from tests.sa_db_settings import sa_repo_config

repos_to_test = (SARepo(sa_repo_config),)


def generate_random_string_id() -> str:
    return "".join(
        (random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"))
        for x in range(64)
    )


# @pytest.mark.parametrize("repo", repos_to_test)
@pytest_asyncio.fixture()
async def insert_values(repo: BaseRepo, init_db):
    now = datetime.now(UTC)

    user = User(
        id=generate_random_string_id(),
        streak=0,
        last_skill_use=now,
        heard_tips=[],
        last_wake_up_time=time(12, 5, 30),
        join_date=now,
        repo=repo,
    )

    new_user = User(
        id=generate_random_string_id(),
        streak=100,
        last_skill_use=None,
        heard_tips=[],
        last_wake_up_time=time(12, 5, 30),
        join_date=now,
        repo=repo,
    )

    await repo.insert_users([user, new_user])

    topic = TipsTopic(
        uuid4(),
        TextWithTTS("Дневные советы", "Дн+евные сов+еты"),
        TextWithTTS(
            "Ну тупо какие-то дневные советы, а почему бы и нет",
            "Ну т+упо как+ие-то дневн+ые сов+еты, а почем+у бы и нет",
        ),
        now,
        repo,
    )

    new_topic = TipsTopic(
        uuid4(),
        TextWithTTS("Newtopic", "Newt+opic"),
        TextWithTTS(
            "Just a new topic, nothing much",
            "Just a new t+opic, n+othing much",
        ),
        datetime.now(),
        repo,
    )

    await repo.insert_tips_topics([topic, new_topic])

    tip = Tip(
        uuid4(),
        short_description=TextWithTTS(
            "Ну тупо какой-то дневной совет, а почему бы и нет",
            "Ну т+упо как+ой-то дневн+ой сов+ет, а почем+у бы и нет",
        ),
        tip_content=TextWithTTS(
            "Ну тупо какой-то дневной совет, а почему бы и нет",
            "Ну т+упо как+ой-то дневн+ой сов+ет, а почем+у бы и нет",
        ),
        tips_topic=topic,
        created_date=now,
        repo=repo,
    )

    await repo.insert_tip(tip)

    activity = Activity(
        uuid4(),
        TextWithTTS("Сходить посрать", "Сходить в окно"),
        occupation_time=timedelta(hours=23, minutes=59, seconds=59),
        created_date=now,
        repo=repo,
    )

    await repo.insert_activity(activity)


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_users(repo: BaseRepo, init_db):
    now = datetime.now()

    user = User(
        id=generate_random_string_id(),
        streak=0,
        last_skill_use=now,
        heard_tips=[],
        last_wake_up_time=time(12, 5, 30),
        join_date=now,
        repo=repo,
    )

    await repo.insert_user(user)

    deleted_user = await repo.delete_user(user)

    assert deleted_user == user

    with pytest.raises(NoSuchEntityInDB):
        await repo.delete_user(user)

    with pytest.raises(NoSuchEntityInDB):
        user.increase_streak()

        await repo.update_user(user)

    assert await repo.get_user_by_id(user._id) is None

    new_user = User(
        id=generate_random_string_id(),
        streak=0,
        last_skill_use=None,
        heard_tips=[],
        last_wake_up_time=time(12, 5, 30),
        join_date=now,
        repo=repo,
    )

    await repo.insert_users([user, new_user])

    users_list = await repo.get_users()

    assert user in users_list and new_user in users_list

    user_from_repo = await repo.get_user_by_id(user._id)

    assert user == user_from_repo


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_activities(repo: BaseRepo, init_db):
    now = datetime.now()

    activity = Activity(
        uuid4(),
        TextWithTTS("Сходить посрать", "Сходить в окно"),
        occupation_time=timedelta(hours=23, minutes=59, seconds=59),
        created_date=now,
        repo=repo,
    )

    await repo.insert_activity(activity)

    deleted_activity = await repo.delete_activity(activity)

    assert deleted_activity == activity

    with pytest.raises(NoSuchEntityInDB):
        await repo.delete_activity(activity)

    with pytest.raises(NoSuchEntityInDB):
        activity.description = TextWithTTS(
            "Huge description", "+Huge description"
        )
        await repo.update_activity(activity)

    assert await repo.get_activity_by_id(activity._id) is None

    new_activity = Activity(
        uuid4(),
        TextWithTTS("Сходить в Лувр", "Сходить в Третьяковку"),
        occupation_time=timedelta(
            hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=1
        ),
        created_date=now,
        repo=repo,
    )

    await repo.insert_activities([activity, new_activity])

    activities_list = await repo.get_activities()

    assert activity in activities_list and new_activity in activities_list

    activity_from_repo = await repo.get_activity_by_id(activity._id)

    assert activity == activity_from_repo


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_tips_topics(repo: BaseRepo, init_db):
    now = datetime.now()

    topic = TipsTopic(
        uuid4(),
        TextWithTTS("Дневные советы", "Дн+евные сов+еты"),
        TextWithTTS(
            "Ну тупо какие-то дневные советы, а почему бы и нет",
            "Ну т+упо как+ие-то дневн+ые сов+еты, а почем+у бы и нет",
        ),
        now,
        repo,
    )

    await repo.insert_tips_topic(topic)

    deleted_tips_topic = await repo.delete_tips_topic(topic)

    assert deleted_tips_topic == topic

    with pytest.raises(NoSuchEntityInDB):
        await repo.delete_tips_topic(topic)

    with pytest.raises(NoSuchEntityInDB):
        topic.topic_description = TextWithTTS(
            "Huge description", "+Huge description"
        )
        await repo.update_tips_topic(topic)

    assert await repo.get_tips_topic_by_id(topic._id) is None

    new_topic = TipsTopic(
        uuid4(),
        TextWithTTS("Newtopic", "Newt+opic"),
        TextWithTTS(
            "Just a new topic, nothing much",
            "Just a new t+opic, n+othing much",
        ),
        datetime.now(),
        repo,
    )

    await repo.insert_tips_topics([topic, new_topic])

    topics_list = await repo.get_tips_topics()

    assert topic in topics_list and new_topic in topics_list

    tips_topic_from_repo = await repo.get_tips_topic_by_id(topic._id)

    assert tips_topic_from_repo == topic


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_tips(repo: BaseRepo, insert_values):
    now = datetime.now()

    tip = Tip(
        uuid4(),
        short_description=TextWithTTS(
            "Ну тупо очередной какой-то дневной совет, а почему бы и нет",
            "Ну т+упо как+ой-то дневн+ой сов+ет, а почем+у бы и нет",
        ),
        tip_content=TextWithTTS(
            "Ну тупо очередной какой-то дневной совет, а почему бы и нет",
            "Ну т+упо как+ой-то дневн+ой сов+ет, а почем+у бы и нет",
        ),
        tips_topic=(await repo.get_tips_topics(1))[0],
        created_date=now,
        repo=repo,
    )

    await repo.insert_tip(tip)

    deleted_tip = await repo.delete_tip(tip)

    assert deleted_tip == tip

    with pytest.raises(NoSuchEntityInDB):
        await repo.delete_tip(tip)

    with pytest.raises(NoSuchEntityInDB):
        tip.short_description = TextWithTTS(
            "Huge description", "+Huge description"
        )
        await repo.update_tip(tip)

    assert await repo.get_tip_by_id(tip._id) is None

    new_tip = Tip(
        uuid4(),
        TextWithTTS(
            "A new description for the tip",
            "A new descr+iption for the tip",
        ),
        TextWithTTS("Its content", "Its c+ontent"),
        (await repo.get_tips_topics(1))[0],
        datetime.now(),
        repo,
    )

    await repo.insert_tips([tip, new_tip])

    tips_list = await repo.get_tips()

    assert tip in tips_list and new_tip in tips_list

    tip_from_repo = await repo.get_tip_by_id(tip._id)

    assert tip_from_repo == tip


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_update(repo: BaseRepo, insert_values):
    activity = (await repo.get_activities(1))[0]

    activity.description = TextWithTTS(
        activity.description.text, activity.description.tts + " Updated now!"
    )

    activity.occupation_time = timedelta(
        hours=0, minutes=0, seconds=0, microseconds=0, milliseconds=1
    )

    updated_activity = await repo.update_activity(activity)

    assert (
        activity._id == updated_activity._id
        and activity.description == updated_activity.description
        and activity.occupation_time == updated_activity.occupation_time
    )

    tips_topic = (await repo.get_tips_topics(1))[0]

    tips_topic.name = TextWithTTS("Newname", "Newn+ame")

    tips_topic.topic_description = TextWithTTS(
        "Just a topic for testing", "Just a t+opic for t+esting"
    )

    updated_tips_topic = await repo.update_tips_topic(tips_topic)

    assert (
        tips_topic._id == updated_tips_topic._id
        and tips_topic.name == updated_tips_topic.name
        and tips_topic.topic_description
        == updated_tips_topic.topic_description
    )

    # TODO Add filtering
    new_topic = list(
        filter(lambda x: x._id != tips_topic._id, await repo.get_tips_topics())
    )[0]

    tip = (await repo.get_tips(1))[0]

    tip.short_description = TextWithTTS(
        "Well, another description goes here",
        "Well, an+other descr+iption goes h+ere",
    )

    tip.tip_content = TextWithTTS(
        "Well, that's the content I'd like to read",
        "Well, that's the c+ontent I'd like to read",
    )

    tip.tips_topic = new_topic

    updated_tip = await repo.update_tip(tip)

    assert (
        tip.short_description == updated_tip.short_description
        and tip.tip_content == updated_tip.tip_content
        and tip.tips_topic == updated_tip.tips_topic
    )

    user = (await repo.get_users(1))[0].increase_streak()

    new_tip = await repo.insert_tip(
        Tip(
            uuid4(),
            TextWithTTS(
                "A new description for the tip",
                "A new descr+iption for the tip",
            ),
            TextWithTTS("Its content", "Its c+ontent"),
            tips_topic,
            datetime.now(),
            repo,
        )
    )

    user.add_heard_tip(new_tip)

    user.last_skill_use = datetime.now()

    user.last_wake_up_time = time(1, 50, 32)

    updated_user = await repo.update_user(user)

    assert user._streak == updated_user._streak

    assert updated_user.last_skill_use == user.last_skill_use.astimezone(
        timezone(timedelta(0))
    )
    assert updated_user.last_wake_up_time == user.last_wake_up_time
    assert new_tip in user._heard_tips
    assert new_tip in updated_user._heard_tips

    user.drop_heard_tips()

    updated_user = await repo.update_user(user)

    assert updated_user._heard_tips == []


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_getting(repo: BaseRepo, insert_values):
    activities = await repo.get_activities()

    assert await repo.get_activity_by_id(activities[0]._id) in activities

    tips = await repo.get_tips()

    assert await repo.get_tip_by_id(tips[0]._id) in tips

    tips_topics = await repo.get_tips_topics()

    assert await repo.get_tips_topic_by_id(tips_topics[0]._id) in tips_topics

    users = await repo.get_users()

    assert await repo.get_user_by_id(users[0]._id) in users

    tips_with_topic = await repo.get_topic_tips(tips_topics[0]._id)

    assert tips_with_topic != []


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_users_stats(repo: BaseRepo, insert_values):
    BIG_STREAK = 10000

    all_users = await repo.get_users()

    all_user_counter = await repo.count_all_users()

    assert len(all_users) == all_user_counter

    assert await repo.count_users_with_streak(BIG_STREAK, condition=">") == 0
    assert await repo.count_users_with_streak(BIG_STREAK, condition=">=") == 0

    assert (
        await repo.count_users_with_streak(BIG_STREAK, condition="<")
        == all_user_counter
    )

    assert (
        await repo.count_users_with_streak(BIG_STREAK, condition="<=")
        == all_user_counter
    )

    assert await repo.count_users_with_streak(100, condition="<") == 1

    assert await repo.count_users_with_streak(100, condition="<=") == 2

    assert await repo.count_users_with_streak(100, condition=">=") == 1

    assert await repo.count_users_with_streak(100, condition="==") == 1

    assert await repo.count_users_with_streak(100, condition=">") == 0

    assert await repo.count_users_with_streak(100, condition="==") == 1


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_deleting_all_users(repo: BaseRepo, insert_values):
    await repo.delete_all_users()

    assert await repo.get_users() == []

    await repo.delete_all_tips_topics()


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_deleting_all_activities(repo: BaseRepo, insert_values):
    await repo.delete_all_activities()

    assert await repo.get_activities() == []


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_deleting_all_tips_topics(repo: BaseRepo, insert_values):
    await repo.delete_all_tips_topics()

    assert await repo.get_tips_topics() == []

    assert await repo.get_tips() == []


@pytest.mark.parametrize("repo", repos_to_test)
@pytest.mark.asyncio
async def test_deleting_all_tips(repo: BaseRepo, insert_values):
    await repo.delete_all_tips_topics()

    topics_before_deleting = await repo.get_tips_topics()

    assert await repo.get_tips() == []

    assert await repo.get_tips_topics() == topics_before_deleting
