import logging

from aiogram import Bot
from aiogram.types import Message, MessageReactionUpdated

from bot.user_topic_context import UserTopicContext

logger: logging.Logger = logging.getLogger(__name__)


async def any_message_reaction(
    reaction: MessageReactionUpdated,
    bot: Bot,
    context: UserTopicContext,
):
    logger.debug("Called any_message_reaction")
    if not context.edit_message_id:
        return

    try:
        await bot.set_message_reaction(
            chat_id=context.edit_chat_id,
            message_id=context.edit_message_id,
            reaction=reaction.new_reaction
        )
    except Exception as ex:
        logger.error(
            "Failed to set message reaction. chat_id: %s, message_id: %s, "
            "exception_type: %s, exception_text: %s",
            context.edit_chat_id,
            context.edit_message_id,
            type(ex),
            str(ex)
        )


async def any_edited_message(
    message: Message,
    bot: Bot,
    context: UserTopicContext,
):
    """
    Handler to edited message anywhere.
    Updates corresponding message in other chat
    (either forum supergroup or PM)

    :param message: message from Telegram
    :param bot: bot instance
    :param context: topic, related to this handler
    """
    if not context.edit_message_id:
        return

    kwargs = {
        "chat_id": context.edit_chat_id,
        "message_id": context.edit_message_id
    }

    if message.text:
        method = bot.edit_message_text
        kwargs.update(text=message.text)
    else:
        method = bot.edit_message_caption
        kwargs.update(caption=message.caption)

    await method(**kwargs)
