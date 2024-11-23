import discord
import logging
from typing import Optional, Tuple
from util import log_info_and_embed, send_dm
from settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


async def ban_user(
    invoking_member: discord.Member,
    user: discord.Member,
    reason: str,
    delete_messages: bool,
) -> Optional[Tuple[bool, bool, str]]:
    """Executes ban of user.

    Args:
        invoking_member (discord.Member): The moderator initiating the ban.
        user (discord.Member): The user being banned.
        reason (str): Reason for the ban.
        delete_messages (bool): Whether to delete the user's messages.

    Returns:
        Optional[Tuple[bool, bool, str]]: Result of the ban operation. Tuple contains:
            - bool: True if ban was successful, False otherwise.
            - bool: True if DM was successfully sent, False otherwise.
            - str: Description of the result of the ban operation
    """
    if len(reason) >= 512:
        return (
            False,
            False,
            f"Unable to ban {user.mention}: reason is too long (above 512 characters). Please shorten the ban reason.",
        )

    # Ensure invoking_member has a higher role position than the target user.
    if user.top_role >= invoking_member.top_role:
        return (
            False,
            False,
            f"Unable to ban {user.mention}: You cannot ban a user with an equal or higher role than yourself.",
        )

    dm_state = False
    try:
        await send_dm(
            user,
            f"You are being banned from NA Ultimate Raiding - FFXIV for the following reason:\n> {reason}\n"
            "You may appeal this ban by contacting the moderators in 30 days.",
        )
        dm_state = True
    except Exception as e:
        logger.error(f"Failed to send DM to {user.mention}: {e}")

    try:
        # Delete messages only if delete_messages is True
        # 604800 seconds is the maximum value for delete_message_seconds, and is equivalent to 7 days.
        delete_seconds = 604800 if delete_messages else 0
        await user.ban(reason=reason, delete_message_seconds=delete_seconds)
        logger.info(f"Successfully banned {user.mention}")
        return (True, dm_state, f"Successfully banned {user.mention}.")
    except Exception as e:
        logger.error(f"Failed to ban {user.mention}: {e}")
        return (
            False,
            dm_state,
            f"Failed to ban {user.mention}. Please try again or use Discord's built-in tools.",
        )
