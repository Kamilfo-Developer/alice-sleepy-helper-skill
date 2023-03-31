from __future__ import annotations
import abc
from uuid import UUID
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    TYPE_CHECKING,
    Iterable,
    Literal,
)

if TYPE_CHECKING:
    from skill.entities import Activity, Tip, TipsTopic, User


class RepoConfig:
    connection_provider: Callable[..., AsyncContextManager[Any]]

    def __init__(
        self, connection_provider: Callable[..., AsyncContextManager[Any]]
    ) -> None:
        self.connection_provider = connection_provider


class BaseRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, config: RepoConfig) -> None:
        pass

    @abc.abstractmethod
    async def insert_user(self, user: User) -> User:
        pass

    @abc.abstractmethod
    async def insert_users(self, users: Iterable[User]) -> list[User]:
        pass

    @abc.abstractmethod
    async def insert_activity(self, activity: Activity) -> Activity:
        pass

    @abc.abstractmethod
    async def insert_activities(
        self, activities: Iterable[Activity]
    ) -> list[Activity]:
        pass

    @abc.abstractmethod
    async def insert_tips_topic(self, tips_topic: TipsTopic) -> TipsTopic:
        pass

    @abc.abstractmethod
    async def insert_tips_topics(
        self, tips_topics: Iterable[TipsTopic]
    ) -> list[TipsTopic]:
        pass

    @abc.abstractmethod
    async def insert_tip(self, tip: Tip) -> Tip:
        pass

    @abc.abstractmethod
    async def insert_tips(self, tips: Iterable[Tip]) -> list[Tip]:
        pass

    @abc.abstractmethod
    async def delete_all_users(self) -> None:
        """Deletes ALL users entities from the db"""
        pass

    @abc.abstractmethod
    async def delete_all_activities(self) -> None:
        """Deletes ALL activities entities from the db"""
        pass

    @abc.abstractmethod
    async def delete_all_tips_topics(self) -> None:
        """Deletes ALL tips topics entities from the db"""
        pass

    @abc.abstractmethod
    async def delete_all_tips(self) -> None:
        """Deletes ALL tips entities from the db"""
        pass

    @abc.abstractmethod
    async def delete_user(self, user: User) -> User:
        """Deletes the passed user entity from the db

        Args:
            user (User): user that is going to be deleted

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            User: deleted entity
        """
        pass

    @abc.abstractmethod
    async def delete_activity(self, activity: Activity) -> Activity:
        """Deletes the passed activity entity from the db

        Args:
            activity (Activity): activity that is going to be deleted

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            Activity: deleted entity
        """
        pass

    @abc.abstractmethod
    async def delete_tips_topic(self, tips_topic: TipsTopic) -> TipsTopic:
        """Deletes the passed tips topic entity from the db
        with all the related tips

        Args:
            tips_topic (TipsTopic): tips topic that is going to be deleted

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            TipsTopic: deleted entity
        """
        pass

    @abc.abstractmethod
    async def delete_tip(self, tip: Tip) -> Tip:
        """Deletes the passed tip entity from the db

        Args:
            tip (Tip): tip that is going to be deleted

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            Tip: deleted entity
        """
        pass

    @abc.abstractmethod
    async def update_user(self, user: User) -> User:
        """Updates the passed user entity in the db

        Args:
            user (User): user that is going to be updated

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            User: updated entity
        """
        pass

    @abc.abstractmethod
    async def update_activity(self, activity: Activity) -> Activity:
        """Updates the passed user entity in the db

        Args:
            activity (User): activity that is going to be updated

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            Activity: updated entity
        """
        pass

    @abc.abstractmethod
    async def update_tips_topic(self, tips_topic: TipsTopic) -> TipsTopic:
        """Updates the passed tips topic entity in the db

        Args:
            tips_topic (TipsTopic): tips topic that is going to be updated

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            TipsTopic: updated entity
        """
        pass

    @abc.abstractmethod
    async def update_tip(self, tip: Tip) -> Tip:
        """Updates the passed tip entity in the db

        Args:
            tip (Tip): tip that is going to be updated

        Raises:
            NoSuchEntityInDB: raised if no such entity in the DB

        Returns:
            Tip: updated entity
        """
        pass

    @abc.abstractmethod
    async def get_user_by_id(self, id: str) -> User | None:
        pass

    @abc.abstractmethod
    async def get_activity_by_id(self, id: UUID) -> Activity | None:
        pass

    @abc.abstractmethod
    async def get_tips_topic_by_id(self, id: UUID) -> TipsTopic | None:
        pass

    @abc.abstractmethod
    async def get_tips_topic_by_name(self, name: str) -> TipsTopic | None:
        pass

    @abc.abstractmethod
    async def get_tip_by_id(self, id: UUID) -> Tip | None:
        pass

    @abc.abstractmethod
    async def get_tips_topics(
        self, limit: int | None = None
    ) -> list[TipsTopic]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[TipsTopic]: list with objects
        """
        pass

    @abc.abstractmethod
    async def get_topic_tips(self, topic_id: UUID) -> list[Tip]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[Tip]: list with objects ordered by creation date

        """
        pass

    @abc.abstractmethod
    async def get_tips(self, limit: int | None = None) -> list[Tip]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[Tip]: list with objects
        """
        pass

    @abc.abstractmethod
    async def get_activities(self, limit: int | None = None) -> list[Activity]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[Activity]: list with objects
        """
        pass

    @abc.abstractmethod
    async def get_users(self, limit: int | None = None) -> list[User]:
        """If no limit provided, the method should return
        all tips topics from the DB

        Args:
            limit (int | None, optional): how many objects you want to get.
            Defaults to None.

        Returns:
            list[User]: list with objects
        """
        pass

    @abc.abstractmethod
    async def count_all_users(self) -> int:
        pass

    @abc.abstractmethod
    async def count_users_with_streak(
        self,
        streak: int,
        condition: Literal["<"]
        | Literal[">"]
        | Literal["<="]
        | Literal[">="]
        | Literal["=="],
    ) -> int:
        pass
