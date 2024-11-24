from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from settings import get_settings

settings = get_settings()


class User(BaseModel):
    user_id: int
    discord_user_id: str
    discord_guild_id: str
    is_mod: bool
    temporary_points: int
    permanent_points: int
    last_infraction_timestamp: Optional[datetime]
