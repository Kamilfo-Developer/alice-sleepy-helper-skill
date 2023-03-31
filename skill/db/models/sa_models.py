from __future__ import annotations
from uuid import UUID
from sqlalchemy import (
    Integer,
    Table,
    Time,
    Uuid,
    ForeignKey,
    DateTime,
    String,
    Interval,
    Column,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from skill.db.repos.base_repo import BaseRepo
from skill.entities import User, Activity, Tip, TipsTopic
from datetime import datetime, time, timedelta
from skill.utils import TextWithTTS


class BaseModel(DeclarativeBase):
    pass


heard_tips_table = Table(
    "heard_tips",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tip_id", ForeignKey("tips.id"), primary_key=True),
)


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    streak: Mapped[int] = mapped_column(Integer)
    last_skill_use: Mapped[datetime | None] = mapped_column(
        DateTime(True), default=None
    )
    last_wake_up_time: Mapped[time | None] = mapped_column(
        Time(), default=None
    )
    join_date: Mapped[datetime] = mapped_column(DateTime(True))

    heard_tips: Mapped[list[TipModel]] = relationship(
        "TipModel",
        back_populates="users_heard",
        order_by="TipModel.created_date",
        lazy="selectin",
        secondary=heard_tips_table,
    )

    def __init__(self, entity: User):
        self.id = entity._id
        self.streak = entity._streak
        self.last_skill_use = entity.last_skill_use
        self.last_wake_up_time = entity.last_wake_up_time
        self.join_date = entity._join_date

        self.heard_tips = [
            TipModel(heard_tip) for heard_tip in entity._heard_tips
        ]

    def as_entity(self, repo: BaseRepo) -> User:
        return User(
            id=self.id,
            streak=self.streak,
            last_skill_use=self.last_skill_use,
            last_wake_up_time=self.last_wake_up_time,
            join_date=self.join_date,
            heard_tips=[tip.as_entity(repo) for tip in self.heard_tips],
            repo=repo,
        )


class ActivityModel(BaseModel):
    __tablename__ = "activities"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    description_text: Mapped[str] = mapped_column(
        String(512), unique=True, index=True
    )
    description_tts: Mapped[str] = mapped_column(String(512))
    created_date: Mapped[datetime] = mapped_column(DateTime(True))
    occupation_time: Mapped[timedelta] = mapped_column(Interval)

    def __init__(self, entity: Activity):
        self.id = entity._id
        self.created_date = entity._created_date
        self.description_text, self.description_tts = (
            entity.description.text,
            entity.description.tts,
        )
        self.occupation_time = entity.occupation_time

    def as_entity(self, repo: BaseRepo) -> Activity:
        return Activity(
            id=self.id,
            created_date=self.created_date,
            description=TextWithTTS(
                self.description_text, self.description_tts
            ),
            occupation_time=self.occupation_time,
            repo=repo,
        )


class TipModel(BaseModel):
    __tablename__ = "tips"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    short_description_text: Mapped[str] = mapped_column(
        String(256), unique=True, index=True
    )
    short_description_tts: Mapped[str] = mapped_column(String(256))
    tip_content_text: Mapped[str] = mapped_column(
        String(1024), unique=True, index=True
    )
    tip_content_tts: Mapped[str] = mapped_column(String(1024))

    tips_topic_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tips_topics.id", ondelete="CASCADE")
    )
    tips_topic = relationship(
        "TipsTopicModel",
        back_populates="tips",
        lazy="selectin",
    )

    users_heard = relationship("UserModel", secondary=heard_tips_table)

    created_date: Mapped[datetime] = mapped_column(DateTime(True))

    def __init__(self, entity: Tip) -> None:
        self.id = entity._id
        self.short_description_text, self.short_description_tts = (
            entity.short_description.text,
            entity.short_description.tts,
        )

        self.tip_content_text, self.tip_content_tts = (
            entity.tip_content.text,
            entity.tip_content.tts,
        )

        self.tips_topic_id = entity.tips_topic._id

        self.created_date = entity._created_date

    def as_entity(self, repo: BaseRepo) -> Tip:
        return Tip(
            id=self.id,
            created_date=self.created_date,
            short_description=TextWithTTS(
                self.short_description_text, self.short_description_tts
            ),
            tip_content=TextWithTTS(
                self.tip_content_text, self.tip_content_tts
            ),
            tips_topic=self.tips_topic.as_entity(repo),
            repo=repo,
        )


class TipsTopicModel(BaseModel):
    __tablename__ = "tips_topics"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name_text: Mapped[str] = mapped_column(
        String(256), unique=True, index=True
    )
    name_tts: Mapped[str] = mapped_column(String(256))
    topic_description_text: Mapped[str] = mapped_column(
        String(1024), unique=True, index=True
    )
    topic_description_tts: Mapped[str] = mapped_column(String(1024))

    tips = relationship(
        "TipModel",
        back_populates="tips_topic",
        passive_deletes=True,
    )

    created_date: Mapped[datetime] = mapped_column(DateTime(True))

    def __init__(self, entity: TipsTopic) -> None:
        self.id = entity._id
        self.name_text, self.name_tts = entity.name.text, entity.name.tts
        self.topic_description_text, self.topic_description_tts = (
            entity.topic_description.text,
            entity.topic_description.tts,
        )
        self.created_date = entity._created_date

    def as_entity(self, repo: BaseRepo) -> TipsTopic:
        return TipsTopic(
            id=self.id,
            created_date=self.created_date,
            name=TextWithTTS(self.name_text, self.name_tts),
            topic_description=TextWithTTS(
                self.topic_description_text, self.topic_description_tts
            ),
            repo=repo,
        )
