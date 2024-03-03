from uuid import UUID, uuid4

from pydantic import Field
from beanie import Document

class Guild(Document):
    class Settings:
        name = "guilds"
    
    id: UUID = Field(default_factory=uuid4)
    guild_id: int
    name: str
    bot_log_channel_id: int