from typing import Any, Awaitable, Callable, Dict
from typing import NamedTuple

import structlog
from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject, Message, ForumTopic
from cachetools import LRUCache
from motor.motor_asyncio import AsyncIOMotorDatabase

log: structlog.BoundLogger = structlog.get_logger()


class NewTopicData(NamedTuple):
    topic_id: int | None
    first_message_id: int | None


class TopicsManagementMiddleware(BaseMiddleware):
    def __init__(self, mongo: AsyncIOMotorDatabase):
        self.mongo = mongo
        self.cache = LRUCache(maxsize=10)

    async def find_topic_by_user(self, user_id: int) -> dict | None:
        # Search in cache // O(1)
        if user_id in self.cache:
            log.debug("User %s found in local cache", user_id)
            return self.cache[user_id]
        user_topic_data = await self.mongo.topics.find_one({"user_id": user_id})
        if user_topic_data:
            # Update cache
            self.cache[user_id] = user_topic_data
            return user_topic_data

    async def find_user_by_topic(self, topic_id: int) -> int | None:
        # Search in cache // O(n), best effort
        for key, value in self.cache.items():
            if value.get("topic_id", -1) == topic_id:
                log.debug("Topic %s found in local cache", topic_id)
                return key
        # Search in mongo
        user_topic_data = await self.mongo.topics.find_one({"topic_id": topic_id})
        if user_topic_data:
            # Update cache
            self.cache[user_topic_data["user_id"]] = user_topic_data
            return user_topic_data["user_id"]

    async def create_new_topic(self, bot: Bot, supergroup_id: int, user_id: int):
        try:
            new_topic: ForumTopic = await bot.create_forum_topic(supergroup_id, f"id{user_id}")
            first_topic_message = await bot.send_message(
                supergroup_id,
                message_thread_id=new_topic.message_thread_id,
                text="Topic created!"  # todo: better first message
            )
        except TelegramBadRequest as ex:
            log.error(
                event="Could not create new topic",
                error_type=ex.__class__.__name__, message=ex.message,
                method=ex.method.__class__.__name__, method_args=ex.method.dict()
            )
            return NewTopicData(None, None)
        else:
            log.debug("Created new topic with id %s", new_topic.message_thread_id)
            self.cache[user_id] = {
                "user_id": user_id,
                "topic_id": new_topic.message_thread_id,
                "first_message_id": new_topic.message_thread_id
            }
            return NewTopicData(new_topic.message_thread_id, first_topic_message.message_id)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # If someone accidentally tried to add this middleware
        # to anything but messages or edited messages, just ignore it
        if not isinstance(event, Message):
            log.warn("%s used not for Message, but for %s", self.__class__.__name__, type(event))
            return await handler(event, data)

        event: Message

        if event.chat.id == data["forum_chat_id"]:
            # If the message comes from forum supergroup, find relevant user id
            user_id = await self.find_user_by_topic(event.message_thread_id)
            data.update(user_id=user_id)
        else:
            topic_info = await self.find_topic_by_user(event.from_user.id)
            if topic_info:
                data.update(
                    topic_id=topic_info["topic_id"],
                    first_message_id=topic_info["first_message_id"]
                )
            else:
                new_topic: NewTopicData = await self.create_new_topic(
                    bot=data["bot"],
                    supergroup_id=data["forum_chat_id"],
                    user_id=event.from_user.id
                )
                data.update(
                    topic_id=new_topic.topic_id,
                    first_message_id=new_topic.first_message_id
                )

                if new_topic.topic_id:
                    await self.mongo.topics.insert_one(
                        {
                            "user_id": event.from_user.id,
                            "topic_id": new_topic.topic_id,
                            "first_message_id": new_topic.first_message_id
                        }
                    )

        return await handler(event, data)