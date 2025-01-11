import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums.chat_type import ChatType
from aiogram.types import TelegramObject, Message, MessageReactionUpdated

from bot.user_topic_context import UserTopicContext, MessageDirection

logger: logging.Logger = logging.getLogger(__name__)


class UserTopicContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.debug("Called UserTopicContextMiddleware. Type of event: %s", type(event.event))
        if isinstance(event.event, (Message, MessageReactionUpdated)):
            # Ignore "service messages" and other irrelevant content types
            if not isinstance(event.event, MessageReactionUpdated):
                if UserTopicContext.is_service_message(event.event):
                    return

            context = UserTopicContext(data.get("event_from_user"))

            if event.event.chat.id == data["forum_chat_id"]:
                context.message_direction = MessageDirection.FORUM_TO_USER
            elif event.event.chat.type == ChatType.PRIVATE:
                context.message_direction = MessageDirection.USER_TO_FORUM
            else:
                logger.debug("Unknown message direction: %s", event.model_dump())
                context.message_direction = MessageDirection.UNKNOWN

            logger.debug("User Topic Context created!")
            data.update(context=context)

            try:
                msg_thread_id = event.event.message.reply_to_message.message_thread_id
                logger.debug(f"Msg Thread ID: {msg_thread_id}")
            except AttributeError:
                pass

        return await handler(event, data)
