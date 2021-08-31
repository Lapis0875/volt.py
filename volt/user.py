from typing import Optional

from volt.abc import Snowflake, JsonObject
from volt.types.type_hint import JSON


class User(Snowflake, JsonObject):
    username: str
    discriminator: str
    avatar_hash: Optional[str]
    bot: Optional[bool]

    @classmethod
    def from_json(cls, data: JSON) -> 'JsonObject':
        pass

    def __init__(self):
        pass

    def to_json(self) -> JSON:
        pass

    @property
    def avatar_url(self) -> str:
        return f'https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.png'
