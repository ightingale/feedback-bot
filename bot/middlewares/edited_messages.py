import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, MessageReactionUpdated

from bot.user_topic_context import UserTopicContext

logger: logging.Logger = logging.getLogger(__name__)


class EditedMessagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.info("Called EditedMessagesMiddleware")
        # If someone accidentally tried to add this middleware
        # to anything but messages, just ignore it
        if not isinstance(event, (Message, MessageReactionUpdated)):
            logger.warning(
                "%s used not for Message, but for %s", self.__class__.__name__, type(event)
            )
            return await handler(event, data)

        event: Message
        context: UserTopicContext = data["context"]

        saved_message = await context.get_message_pair(
            is_from_bot=False if isinstance(event, Message) else True,
            chat_id=event.chat.id,
            message_id=event.message_id
        )
        logger.debug("Attempted to get message pair for edited message")
        if saved_message is not None:
            if isinstance(event, Message):
                context.edit_chat_id = saved_message.to_chat_id
                context.edit_message_id = saved_message.to_message_id
            else:
                context.edit_chat_id = saved_message.from_chat_id
                context.edit_message_id = saved_message.from_message_id
        return await handler(event, data)
