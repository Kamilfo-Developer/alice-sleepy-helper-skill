from __future__ import annotations
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from skill.db.repos.base_repo import BaseRepo
from skill.utils import IdComparable, TextWithTTS


class User(IdComparable):
    _id: str
    _streak: int
    lask_skill_use: datetime | None
    _heard_tips: list[Tip]
    _join_date: datetime

    def __init__(
        self,
        id: str,
        streak: int,
        last_skill_use: datetime | None,
        heard_tips: list[Tip],
        join_date: datetime,
        repo: BaseRepo,
    ) -> None:
        self._id = id
        self._streak = streak
        self.last_skill_use = last_skill_use
        self._heard_tips = heard_tips
        self._join_date = join_date
        self.__repo = repo

    def increase_streak(self) -> User:
        self._streak += 1

        return self

    def drop_streak(self) -> User:
        self._streak = 0

        return self

    def drop_heard_tips(self) -> User:
        self._heard_tips = []

        return self

    def add_heard_tip(self, tip: Tip) -> User:
        self._heard_tips.append(tip)

        return self


class Activity(IdComparable):
    _id: UUID
    _created_date: datetime
    occupation_time: timedelta

    # description: TextWithTTS
    @property
    def description(self) -> TextWithTTS:
        return self.__description

    @description.setter
    def description(self, value: TextWithTTS):
        if len(max(value.text, value.tts, key=len)) > 512:
            raise ValueError(
                "Text and its speech format lengths should both be < 512"
            )

        self.__description = value

    def __init__(
        self,
        id: UUID,
        description: TextWithTTS,
        created_date: datetime,
        occupation_time: timedelta,
        repo: BaseRepo,
    ) -> None:
        self._id = id
        self.description = description
        self.occupation_time = occupation_time
        self._created_date = created_date
        self.__repo = repo


class Tip(IdComparable):
    _id: UUID
    _created_date: datetime
    tips_topic: TipsTopic

    # short_description: TextWithTTS
    @property
    def short_description(self) -> TextWithTTS:
        return self.__short_description

    @short_description.setter
    def short_description(self, value: TextWithTTS):
        if len(max(value.text, value.tts, key=len)) > 256:
            raise ValueError(
                "Text and its speech format lengths should both be < 256"
            )

        self.__short_description = value

    # tip_content: TextWithTTS
    @property
    def tip_content(self) -> TextWithTTS:
        return self.__tip_content

    @tip_content.setter
    def tip_content(self, value: TextWithTTS):
        if len(max(value.text, value.tts, key=len)) > 1024:
            raise ValueError(
                "Text and its speech format lengths should both be < 1024"
            )

        self.__tip_content = value

    def __init__(
        self,
        id: UUID,
        short_description: TextWithTTS,
        tip_content: TextWithTTS,
        tips_topic: TipsTopic,
        created_date: datetime,
        repo: BaseRepo,
    ) -> None:
        self._id = id
        self.short_description = short_description
        self.tip_content = tip_content
        self._created_date = created_date
        self.tips_topic = tips_topic
        self.__repo = repo


class TipsTopic(IdComparable):
    _id: UUID
    _created_date: datetime

    # name: TextWithTTS
    @property
    def name(self) -> TextWithTTS:
        return self.__name

    @name.setter
    def name(self, value: TextWithTTS):
        if len(max(value.text, value.tts, key=len)) > 1024:
            raise ValueError(
                "Text and its speech format lengths should both be < 1024"
            )

        self.__name = value

    # topic_description: TextWithTTS
    @property
    def topic_description(self) -> TextWithTTS:
        return self.__topic_description

    @topic_description.setter
    def topic_description(self, value: TextWithTTS):
        if len(max(value.text, value.tts, key=len)) > 1024:
            raise ValueError(
                "Text and its speech format lengths should both be < 1024"
            )

        self.__topic_description = value

    def __init__(
        self,
        id: UUID,
        name: TextWithTTS,
        topic_description: TextWithTTS,
        created_date: datetime,
        repo: BaseRepo,
    ) -> None:
        self._id = id
        self.name = name
        self.topic_description = topic_description
        self._created_date = created_date
        self.__repo = repo

    async def get_all_tips(self) -> list[Tip]:
        return await self.__repo.get_topic_tips(self._id)

    async def add_tip(
        self,
        short_description: TextWithTTS,
        tip_content: TextWithTTS,
        tips_topic: TipsTopic,
        created_date: datetime,
    ) -> Tip:
        return await self.__repo.insert_tip(
            Tip(
                id=uuid4(),
                short_description=short_description,
                tip_content=tip_content,
                tips_topic=tips_topic,
                created_date=created_date,
                repo=self.__repo,
            )
        )
