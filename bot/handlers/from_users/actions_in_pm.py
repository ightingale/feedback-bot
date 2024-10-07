from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.config_reader import AppConfig


async def cmd_start(message: Message, l10n: FluentLocalization, bot_config: AppConfig):
    """
    Handler to /start commands in PM with user

    :param message: message from Telegram
    :param l10n: FluentLocalization object
    :param bot_config: Application Config
    """
    text = l10n.format_value(
            "start-text",
            {
                "bot_info": bot_config.bot.info
            }
        )
    await message.answer(text)


def get_router() -> Router:
    router = Router(name="actions_in_pm")
    router.message.register(cmd_start, F.text, CommandStart())

    return router
