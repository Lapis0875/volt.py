from enum import IntFlag, IntEnum
from typing import Optional, List

from volt.abc import Snowflake, JsonObject
from volt.types.type_hint import JSON


class ApplicationFlags(IntFlag):
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17


class TeamMemberState(IntEnum):
    INVITED = 1
    ACCEPTED = 2


class TeamMember(JsonObject):
    """

    """
    membership_state: TeamMemberState
    permissions: List[str]
    team_id: int
    user: 'User'


class Team(Snowflake, JsonObject):
    """
    Discord Team object.
    """
    icon: Optional[str]
    members: List[TeamMember]
    name: str
    owner_user_id: int

    __slots__ = ()

    @classmethod
    def from_json(cls, data: JSON) -> 'JsonObject':
        pass

    def __init__(self):
        pass

    def to_json(self) -> JSON:
        pass


class Application(Snowflake, JsonObject):
    """
    Discord Application Object
    """

    __slots__ = ()
    name: str
    icon: Optional[str]
    description: str
    rpc_origins: Optional[List[str]]
    bot_public: bool
    bot_require_code_grant: bool
    terms_of_service_url: Optional[str]
    privacy_policy_url: Optional[str]
    owner: Optional['User']     # partial user object containing info on the owner of the application
    summary: str                # if this application is a game sold on Discord, this field will be the summary field for the store page of its primary sku
    verify_key: str             # the hex encoded key for verification in interactions and the GameSDK's GetTicket
    team: Team                  # if the application belongs to a team, this will be a list of the members of that team
    guild_id: Optional[int]     # if this application is a game sold on Discord, this field will be the guild to which it has been linked
    primary_sku_id: Optional[int]
    slug: Optional[str]
    cover_image: Optional[str]
    flags: ApplicationFlags

    @classmethod
    def from_json(cls):
        pass

    def __init__(self):
        pass

    def to_json(self) -> JSON:
        pass
