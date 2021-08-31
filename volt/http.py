from typing import Final, Optional


class ApiRoute:
    base: Final[str] = ''

    def __init__(self, version: int = 9):
        self.version: Final[int] = version
        self.channel_id: Optional[int] = None
        self.guild_id: Optional[int] = None
        self.user_id: Optional[int] = None
        self.message_id: Optional[int] = None

    def channel(self, channel_id: int) -> 'ApiRoute':
        self.channel_id = channel_id
        return self     # Support method chaining

    def guild(self, guild_id: int) -> 'ApiRoute':
        self.guild_id = guild_id
        return self     # Support method chaining

    def user(self, user_id: int) -> 'ApiRoute':
        self.user_id = user_id
        return self     # Support method chaining

    def message(self, message_id: int) -> 'ApiRoute':
        self.message_id = message_id
        return self     # Support method chaining
