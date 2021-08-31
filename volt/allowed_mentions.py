import typing
from dataclasses import dataclass
from enum import Enum, auto

from volt.abc import JsonObject
from volt.types.type_hint import JSON


class AllowedMentionType(Enum):
    """
    Allowed Mention Types
    """

    @staticmethod
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    Roles = auto()
    Users = auto()
    Everyone = auto()

    @classmethod
    def from_value(cls, value: str) -> 'AllowedMentionType':
        """
        Get AllowedMentionType Enum from value.
        :param value: value to get AllowedMentionType Enum.
        :return: AllowedMentionType Enum if exist, ValueError is raised if value not exist.
        """
        m = cls.__members__.get(value.capitalize())
        if m:
            return m
        else:
            raise ValueError(f'AllowedMentionType with value {value} does not exist!')


@dataclass(init=True, eq=True, repr=True)
class AllowedMentions(JsonObject):
    parse: typing.List[AllowedMentionType]  # An array of allowed mention types to parse from the content.
    roles: typing.List[int]     # Array of role_ids to mention (Max size of 100)
    users: typing.List[int]     # Array of user_ids to mention (Max size of 100)
    replied_user: bool = False  # For replies, whether to mention the author of the message being replied to (default false)

    @classmethod
    def from_json(cls, data: JSON) -> 'JsonObject':
        return cls(
            list(map(AllowedMentionType.from_value, data['parse'])),
            data.get('roles'),
            data.get('users'),
            data.get('replied_user', False)
        )

    def to_json(self) -> JSON:
        pass