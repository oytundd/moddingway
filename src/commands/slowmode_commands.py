import discord
import logging
from discord.ext.commands import Bot
from settings import get_settings
from services.slowmode_service import edit_slowmode
from util import is_user_moderator
from .helper import create_logging_embed, create_response_context

settings = get_settings()
logger = logging.getLogger(__name__)

def create_slowmode_commands(bot: Bot) -> None:
    @bot.tree.command()
    @discord.app_commands.check(is_user_moderator)
    @discord.app_commands.describe(
        channel="Channel name slowmode is being modified in",
        interval="The number of seconds desired between each message. Must be between 0 (off) and 21600 (6 hours).",
    )
    async def set_slowmode(interaction: discord.Interaction, interval: int, channel: discord.TextChannel = None):
        """Set the slowmode interval for the specified channel."""
        async with create_response_context(interaction) as response_message:
            async with create_logging_embed(interaction, interval=interval, channel=channel) as logging_embed:
                result = await edit_slowmode(logging_embed, channel, interval)
                response_message.set_string(result)

