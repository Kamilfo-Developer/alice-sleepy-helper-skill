from typing import Callable, Iterable, Literal
from sqlalchemy import select, func
from skill.db.models.sa_models import (
    ActivityModel,
    TipModel,
    TipsTopicModel,
    UserModel,
)
from skill.db.repos.base_repo import BaseRepo, RepoConfig
from sqlalchemy.ext.asyncio import AsyncSession
from skill.entities import Activity, Tip, TipsTopic, User
from uuid import UUID
import asyncio

from skill.exceptions import IncorrectConditionError


class SARepoConfig(RepoConfig):
    connection_provider: Callable[..., AsyncSession]

    def __init__(
        self, connection_provider: Callable[..., AsyncSession]
    ) -> None:
        self.connection_provider = connection_provider


class SARepo(BaseRepo):
    def __init__(self, config: SARepoConfig) -> None:
        self.__config = config

    async def insert_user(self, user: User) -> User:
        async with self.__config.connection_provider() as session:
            model = UserModel(user)

            session.add(model)

            await session.commit()

            return await self.get_user_by_id(model.id)  # type: ignore

    async def insert_users(self, users: Iterable[User]) -> list[User]:
        async with self.__config.connection_provider() as session:
            models = [UserModel(user) for user in users]

            session.add_all(models)

            await session.commit()

            return [
                entity
                for entity in await asyncio.gather(
                    *[self.get_user_by_id(model.id) for model in models]
                )
            ]  # type: ignore

    async def insert_activity(self, activity: Activity) -> Activity:
        async with self.__config.connection_provider() as session:
            model = ActivityModel(activity)

            session.add(model)

            await session.commit()

            return await self.get_activity_by_id(model.id)  # type: ignore

    async def insert_activities(
        self, activities: Iterable[Activity]
    ) -> list[Activity]:
        async with self.__config.connection_provider() as session:
            models = [ActivityModel(activity) for activity in activities]

            session.add_all(models)

            await session.commit()

            return [
                entity
                for entity in await asyncio.gather(
                    *[self.get_activity_by_id(model.id) for model in models]
                )
            ]  # type: ignore

    async def insert_tips_topic(self, tips_topic: TipsTopic) -> TipsTopic:
        async with self.__config.connection_provider() as session:
            model = TipsTopicModel(tips_topic)

            session.add(model)

            await session.commit()

            return await self.get_tips_topic_by_id(model.id)  # type: ignore

    async def insert_tips_topics(
        self, tips_topics: Iterable[TipsTopic]
    ) -> list[TipsTopic]:
        async with self.__config.connection_provider() as session:
            models = [TipsTopicModel(tips_topic) for tips_topic in tips_topics]

            session.add_all(models)

            await session.commit()

            return [
                entity
                for entity in await asyncio.gather(
                    *[self.get_tips_topic_by_id(model.id) for model in models]
                )
            ]  # type: ignore

    async def insert_tip(self, tip: Tip) -> Tip:
        async with self.__config.connection_provider() as session:
            model = TipModel(tip)

            session.add(model)

            await session.commit()

            return await self.get_tip_by_id(model.id)  # type: ignore

    async def insert_tips(self, tips: Iterable[Tip]) -> list[Tip]:
        async with self.__config.connection_provider() as session:
            models = [TipModel(tip) for tip in tips]

            session.add_all(models)

            await session.commit()

            return [
                entity
                for entity in await asyncio.gather(
                    *[self.get_tip_by_id(model.id) for model in models]
                )
            ]  # type: ignore

    async def delete_user(self, user: User) -> User | None:
        async with self.__config.connection_provider() as session:
            model = await session.get(UserModel, user._id)

            if model:
                await session.delete(model)

                await session.commit()

                return model.as_entity(self)

            return None

    async def delete_activity(self, activity: Activity) -> Activity | None:
        async with self.__config.connection_provider() as session:
            model = await session.get(ActivityModel, activity._id)

            if model:
                await session.delete(model)

                await session.commit()

                return model.as_entity(self)

            return None

    async def delete_tips_topic(
        self, tips_topic: TipsTopic
    ) -> TipsTopic | None:
        async with self.__config.connection_provider() as session:
            model = await session.get(TipsTopicModel, tips_topic._id)

            if model:
                await session.delete(model)

                await session.commit()

                return model.as_entity(self)

            return None

    async def delete_tip(self, tip: Tip) -> Tip | None:
        async with self.__config.connection_provider() as session:
            model = await session.get(TipModel, tip._id)

            if model:
                await session.delete(model)

                await session.commit()

                return model.as_entity(self)

            return None

    async def update_user(self, user: User) -> User:
        async with self.__config.connection_provider() as session:
            model = UserModel(user)

            await session.merge(model)

            await session.commit()

            return await self.get_user_by_id(model.id)  # type: ignore

    async def update_activity(self, activity: Activity) -> Activity:
        async with self.__config.connection_provider() as session:
            model = ActivityModel(activity)

            await session.merge(model)

            await session.commit()

            return await self.get_activity_by_id(model.id)  # type: ignore

    async def update_tips_topic(self, tips_topic: TipsTopic) -> TipsTopic:
        async with self.__config.connection_provider() as session:
            model = TipsTopicModel(tips_topic)

            await session.merge(model)

            await session.commit()

            return await self.get_tips_topic_by_id(model.id)  # type: ignore

    async def update_tip(self, tip: Tip) -> Tip:
        async with self.__config.connection_provider() as session:
            model = TipModel(tip)

            await session.merge(model)

            await session.commit()

            return await self.get_tip_by_id(model.id)  # type: ignore

    async def get_user_by_id(self, id: str) -> User | None:
        async with self.__config.connection_provider() as session:
            q = select(UserModel).where(UserModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_activity_by_id(self, id: UUID) -> Activity | None:
        async with self.__config.connection_provider() as session:
            q = select(ActivityModel).where(ActivityModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_tips_topic_by_id(self, id: UUID) -> TipsTopic | None:
        async with self.__config.connection_provider() as session:
            q = select(TipsTopicModel).where(TipsTopicModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_tips_topic_by_name(self, name: str) -> TipsTopic | None:
        async with self.__config.connection_provider() as session:
            q = select(TipsTopicModel).where(TipsTopicModel.name_text == name)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_tip_by_id(self, id: UUID) -> Tip | None:
        async with self.__config.connection_provider() as session:
            q = select(TipModel).where(TipModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_tips_topics(
        self, limit: int | None = None
    ) -> list[TipsTopic]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[TipsTopic]: list with objects ordered by creation date
        """
        async with self.__config.connection_provider() as session:
            q = (
                select(TipsTopicModel)
                .order_by(TipsTopicModel.created_date)
                .limit(limit)
            )

            res = (await session.execute(q)).scalars().all()

            return [model.as_entity(self) for model in res]

    async def get_topic_tips(
        self, topic_id: UUID, limit: int | None = None
    ) -> list[Tip]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[Tip]: list with objects ordered by creation date

        """
        async with self.__config.connection_provider() as session:
            q = (
                select(TipModel)
                .where(TipModel.tips_topic_id == topic_id)
                .order_by(TipModel.created_date)
                .limit(limit)
            )

            res = (await session.execute(q)).scalars().all()

            return [model.as_entity(self) for model in res]

    async def get_tips(self, limit: int | None = None) -> list[Tip]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[Tip]: list with objects ordered by creation date
        """
        async with self.__config.connection_provider() as session:
            q = select(TipModel).order_by(TipModel.created_date).limit(limit)

            res = (await session.execute(q)).scalars().all()

            return [model.as_entity(self) for model in res]

    async def get_activities(self, limit: int | None = None) -> list[Activity]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[Activity]: list with objects ordered by creation date
        """
        async with self.__config.connection_provider() as session:
            q = (
                select(ActivityModel)
                .order_by(ActivityModel.created_date)
                .limit(limit)
            )

            res = (await session.execute(q)).scalars().all()

            return [model.as_entity(self) for model in res]

    async def get_users(self, limit: int | None = None) -> list[User]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[User]: list with objects ordered by joining date
        """
        async with self.__config.connection_provider() as session:
            q = select(UserModel).order_by(UserModel.join_date).limit(limit)

            res = (await session.execute(q)).scalars().all()

            return [model.as_entity(self) for model in res]

    async def count_all_users(self) -> int:
        async with self.__config.connection_provider() as session:
            q = select(func.count(UserModel.id))

            return (await session.execute(q)).scalar()  # type: ignore

    async def count_users_with_streak(
        self,
        streak: int,
        condition: Literal["<"]
        | Literal[">"]
        | Literal["<="]
        | Literal[">="]
        | Literal["=="],
    ) -> int:
        async with self.__config.connection_provider() as session:
            Q_CONDITIONS = {
                ">": UserModel.streak > streak,
                "<": UserModel.streak < streak,
                ">=": UserModel.streak >= streak,
                "<=": UserModel.streak <= streak,
                "==": UserModel.streak == streak,
            }

            if condition not in Q_CONDITIONS:
                raise IncorrectConditionError()

            q = select(func.count(UserModel.id)).where(Q_CONDITIONS[condition])

            return (await session.execute(q)).scalar()  # type: ignore
