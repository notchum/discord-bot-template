from uuid import UUID, uuid4

from pydantic import Field
from beanie import Document


class BotSettings(Document):
    class Settings:
        name = "settings"

    id: UUID = Field(default_factory=uuid4)
    toggle: bool  # example field for global settings, just a toggle
