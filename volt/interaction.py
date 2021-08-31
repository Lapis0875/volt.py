import aiohttp
from typing import Optional, List, Any, Dict, Mapping, Union

from enum import Enum, IntFlag

from .abc import JsonObject
from .components import ComponentType, Component
from .message import Message
from .types.type_hint import JSON


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3

    @classmethod
    def from_value(cls, value: int) -> Optional['InteractionType']:
        return next(filter(lambda m: m.value == value, cls.__members__.values()), None)


class InteractionData(JsonObject):
    """
    Parent class of all interaction data object. This must be implemented in each interaction api (slash commands, message components, ...)
    """

    @classmethod
    def from_dict(cls, data: JSON):
        raise NotImplemented()

    def to_dict(self) -> JSON:
        raise NotImplemented()


class ApplicationCommandInteractionDataResolved(JsonObject):
    users: Optional[Mapping[int, discord.User]]
    members: Optional[Mapping[int, discord.Member]]
    roles: Optional[Mapping[int, discord.Role]]
    channels: Optional[Mapping[int, AnyChannel]]

    @classmethod
    def resolve_channel(cls, channel_data, bot: discord.Client, guild: Optional[discord.Guild]) -> AnyChannel:
        state = bot._connection
        channel_type: int = channel_data['type']
        if channel_type == discord.ChannelType.text.value:
            return discord.TextChannel(state=state, data=channel_data, guild=guild)
        elif channel_type == discord.ChannelType.private.value:
            return discord.DMChannel(state=state, data=channel_data, me=bot.user)
        elif channel_type == discord.ChannelType.voice.value:
            return discord.VoiceChannel(state=state, data=channel_data, guild=guild)
        elif channel_type == discord.ChannelType.group.value:
            return discord.GroupChannel(state=state, data=channel_data, me=bot.user)
        elif channel_type == discord.ChannelType.category.value:
            return discord.CategoryChannel(state=state, data=channel_data, guild=guild)
        elif channel_type == discord.ChannelType.news.value:
            return discord.TextChannel(state=state, data=channel_data, guild=guild)
        elif channel_type == discord.ChannelType.store.value:
            return discord.StoreChannel(state=state, data=channel_data, guild=guild)
        elif channel_type == 10:  # GUILD_NEWS_THREAD
            raise NotImplemented(
                'Thread channel is not implemented in discord.py, and discord.py-interactions are not ready for this channel.')
        elif channel_type == 11:  # GUILD_PUBLIC_THREAD
            raise NotImplemented(
                'Thread channel is not implemented in discord.py, and discord.py-interactions are not ready for this channel.')
        elif channel_type == 12:  # GUILD_PRIVATE_THREAD
            raise NotImplemented(
                'Thread channel is not implemented in discord.py, and discord.py-interactions are not ready for this channel.')
        elif channel_type == 13:  # GUILD_STAGE_VOICE
            return discord.StageChannel(state=state, data=channel_data, guild=guild)

    @classmethod
    def from_dict(cls, data: JSON, bot: discord.Client,
                  guild: Optional[discord.Guild]) -> 'ApplicationCommandInteractionDataResolved':
        if 'users' in data:
            users = dict(map(
                lambda user_id, user_data: (
                    user_id,
                    bot.get_user(user_id) or discord.User(state=bot._connection, data=user_data)
                ),
                data['users'].items()
            ))
        else:
            users = None

        if 'members' in data:
            members = dict(map(
                lambda member_id, partial_member_data: (
                    member_id,
                    guild.get_member(member_id) if guild is not None
                    else discord.Member(data=partial_member_data, guild=guild, state=bot._connection)
                ),
                data['members'].items()
            ))
        else:
            members = None

        if 'roles' in data:
            roles = dict(map(
                lambda role_id, role_data: (
                    role_id,
                    guild.get_role(role_id) if guild is not None
                    else discord.Role(guild=guild, state=bot._connection, data=role_data)
                ),
                data['roles'].items()
            ))
        else:
            roles = None

        if 'channels' in data:
            channels = dict(map(
                lambda channel_id, partial_channel_data: (
                    channel_id,
                    guild.get_channel(channel_id) if guild is not None
                    else cls.resolve_channel(partial_channel_data, bot, guild)
                ),
                data['channels']
            ))
        else:
            channels = None

        return cls(users, members, roles, channels)

    def __init__(
            self,
            users: Optional[Dict[int, discord.User]],
            members: Optional[Dict[int, discord.Member]],
            roles: Optional[Dict[int, discord.Role]],
            channels: Optional[Dict[int, AnyChannel]]
    ):
        self.users = users
        self.members = members
        self.roles = roles
        self.channels = channels

    def to_dict(self) -> JSON:
        raise NotImplemented('Currently, ApplicationCommandInteractionDataResolved.to_dict() is not implemented. Do we need this method?')


class ApplicationCommandInteractionDataOption(JsonObject):
    @classmethod
    def from_dict(cls, data: JSON) -> 'ApplicationCommandInteractionDataOption':
        value = data.get('value')
        raw_option = data.get('option')
        if value is not None and raw_option is not None:
            raise ValueError('ApplicationCommandInteractionDataOption cannot have both value and option.')

        option = ApplicationCommandInteractionDataOption.from_dict(raw_option) if raw_option is not None else None

        return cls(
            name=data['name'],
            value=value,
            option=option
        )

    def __init__(
            self,
            name: str,
            value: Optional[Any] = None,
            option: Optional[List['ApplicationCommandInteractionDataOption']] = None
    ) -> None:
        self._name: str = name
        self._value: Optional[Any] = value
        self._option: Optional[List[ApplicationCommandInteractionDataOption]] = option

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    @property
    def option(self) -> Optional[List['ApplicationCommandInteractionDataOption']]:
        return self._option

    def to_dict(self) -> JSON:
        data = {'name': self._name}
        if self._value is not None:
            data.update(value=self._value)

        if self._option is not None:
            data.update(option=[o.to_dict() for o in self._option])


class ApplicationCommandInteractionData(JsonObject):
    id: int
    name: str
    resolved: Optional[ApplicationCommandInteractionDataOption]
    options: Optional[List[ApplicationCommandInteractionDataOption]]

    @classmethod
    def from_dict(cls, data: JSON) -> 'ApplicationCommandInteractionData':
        return cls(
            id=data['id'],
            name=data['name'],
            resolved=ApplicationCommandInteractionDataResolved.from_dict(data['resolved']) if 'resolved' in data else None,
            options=list(map(ApplicationCommandInteractionDataOption.from_dict, data['options'])) if 'options' in data else None
        )

    def __init__(
            self,
            id: int,
            name: str,
            resolved: Optional[ApplicationCommandInteractionDataResolved] = None,
            options: Optional[List[ApplicationCommandInteractionDataOption]] = None
    ):
        self.id = id
        self.name = name
        self.resolved = resolved
        self._options: Optional[List[ApplicationCommandInteractionDataOption]] = options

    def getOptions(self) -> Optional[Dict[str, ApplicationCommandInteractionDataOption]]:
        if self._options is not None:
            options_map = {o.name: o for o in self._options}
            # TODO : Implement command invoke logic.
            # TODO : Finish parsing options of interaction to Dict[str, ApplicationCommandInteractionDataOption]
            return options_map
        else:
            return None

    def to_dict(self) -> JSON:
        data = {}
        data.update(
            id=self.id,
            name=self.name
        )
        if self.resolved is not None:
            #
            pass
        if self.options is not None:
            data['options'] = list(map(lambda o: o.to_json(), self.options))
        if self._options is not None:
            data.update(options=[o.to_dict() for o in self._options])

        return data


class MessageComponentsInteractionData(InteractionData):
    custom_id: str
    component_type: ComponentType

    @classmethod
    def from_dict(cls, data: JSON) -> 'MessageComponentsInteractionData':
        return cls(
            data['custom_id'],
            data['component_type']
        )

    def __init__(
            self,
            custom_id: str,
            component_type: ComponentType
    ):
        self.custom_id = custom_id
        self.component_type = component_type

    def to_dict(self) -> JSON:
        return {
            'custom_id': self.custom_id,
            'component_type': self.component_type.value
        }


class Interaction(JsonObject):
    """
    Interaction object.
    """
    id: int
    application_id: int
    type: InteractionType
    token: str
    version: int

    # 'ApplicationCommandInteractionData' object in slash command interaction,
    # 'MessageComponentInteractionData' in message components interaction.
    data: InteractionData

    message: Optional[discord.Message]
    guild_id: Optional[int]
    channel_id: Optional[int]
    # member field is sent when interaction is invoked in guild. In other cases, user field is sent.
    member: Optional[discord.Member]
    user: Optional[discord.User]

    @classmethod
    async def from_dict(cls, data: JSON, bot: discord.Client) -> 'Interaction':
        interaction_type = InteractionType.from_value(data['type'])
        message = ComponentMessage.from_json(data['message'], bot) if 'message' in data else None

        if 'member' in data:
            guild_id = data['guild_id']
            guild = bot.get_guild(guild_id) or await bot.fetch_channel(guild_id) or None
            member = guild.get_member(data['member']['user']['id']) or discord.Member(data=data['member'], guild=guild,
                                                                                      state=bot._connection)
            user = member._user
        elif 'user' in data:
            member = None
            user = bot.get_user(data['user']['id']) or discord.User(data=data['user'], state=bot._connection)
        else:
            member = None
            user = None
        if interaction_type == InteractionType.MESSAGE_COMPONENT:
            # Message Components Interaction
            interaction_data = MessageComponentsInteractionData.from_dict(data['data'])
        elif interaction_type == InteractionType.APPLICATION_COMMAND:
            # Application Command Interaction
            interaction_data = ApplicationCommandInteractionData.from_dict(data['data'])
        else:
            raise ValueError('Unsupported Interaction Data! Please make an issue on github repository.')

        return cls(
            id=data['id'],
            application_id=data['application_id'],
            type=interaction_type,
            data=interaction_data,
            token=data['token'],
            version=data['version'],
            message=message,
            guild_id=data.get('guild_id'),
            channel_id=data.get('channel_id'),
            member=member,
            user=user
        )

    def __init__(
            self,
            id: int,
            application_id: int,
            type: InteractionType,
            data: InteractionData,
            token: str,
            version: int,
            message: Optional[discord.Message] = None,
            guild_id: Optional[discord.Message] = None,
            channel_id: Optional[discord.Message] = None,
            member: Optional[discord.Member] = None,
            user: Optional[discord.User] = None
    ) -> None:
        self.id = id
        self.application_id = application_id
        self.type = type
        self.token = token
        self.version = version
        self.message = message
        self.guild_id = guild_id
        self.channel_id = channel_id
        if member:
            self.member = member
        if user:
            self.user = user
        self.data = data

    async def respond(
            self,
            response: 'InteractionResponse'
    ):
        url = 'https://discord.com/api/v8/interactions/{0}/{1}/callback'.format(self.id, self.token)
        async with aiohttp.ClientSession() as s:
            async with s.post(
                    url,
                    json=response.to_dict()
            ) as resp:
                print(await resp.json())

    def to_dict(self) -> JSON:
        data = {}
        data.update(
            id=self.id,
            application_id=self.application_id,
            type=self.type.value,
            data=self.data.to_dict(),
            token=self.token,
            version=self.version,
            member=self.member,
            user=self.user,
            guild_id=self.guild_id,
            channel_id=self.channel_id,
        )
        return data


class InteractionCallbackType(Enum):
    PONG = 1
    # 2~3 is now not listed on docs. This is implemented when they are listed in docs.
    ACKNOWLEDGE = 2
    CHANNEL_MESSAGE = 3

    CHANNEL_MESSAGE_WITH_SOURCE = 4
    ACKNOWLEDGE_WITH_SOURCE = 5
    # 6~7 is only available in Message Components Interaction.
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7

    @classmethod
    def from_value(cls, value: int) -> 'InteractionCallbackType':
        return next(filter(lambda m: m.value == value, cls.__members__.values()), None)


class InteractionCallbackDataFlags(IntFlag):
    """Interaction Callback Data Flags."""
    # this message has been published to subscribed channels (via Channel Following)
    CROSSPOSTED = 1 << 0

    # this message originated from a message in another channel (via Channel Following)
    IS_CROSSPOST = 1 << 1

    # do not include any embeds when serializing this message
    SUPPRESS_EMBEDS = 1 << 2

    # the source message for this crosspost has been deleted (via Channel Following)
    SOURCE_MESSAGE_DELETED = 1 << 3

    # this message came from the urgent message system
    URGENT = 1 << 4

    # Only author can see message. Hidden to others. Example : Clyde's message
    EPHEMERAL = 1 << 6


class InteractionCallbackData(JsonObject):
    tts: Optional[bool]
    content: Optional[str]
    embeds: Optional[List[discord.Embed]]
    allowed_mentions: Optional[discord.AllowedMentions]
    flags: Optional[InteractionCallbackDataFlags]
    components: Optional[List[ActionRow]]

    @classmethod
    def from_dict(cls, data: JSON) -> 'InteractionCallbackData':
        return cls(
            data.get('tts'),
            data.get('content'),
            list(map(discord.Embed.from_json, data.get('embeds'))) if 'embeds' in data else None,
            discord.AllowedMentions(everyone=data['allowed_mentions']),
            list(map(ActionRow.from_json, data['components'])) if 'components' in data else None
        )

    def __init__(
            self,
            tts: Optional[bool] = None,
            content: Optional[str] = None,
            embeds: Optional[List[discord.Embed]] = None,
            allowed_mentions: Optional[discord.AllowedMentions] = None,
            components: Optional[List[ActionRow]] = None
    ):
        self.tts = tts
        self.content = content
        self.embeds = embeds
        self.allowed_mentions = allowed_mentions
        self.components = components

    def to_dict(self) -> JSON:
        data = {}
        if self.tts is not None:
            data['tts'] = self.tts
        if self.content is not None:
            data['content'] = self.content
        if self.embeds is not None:
            data['embeds'] = list(map(lambda e: e.to_json(), self.embeds))
        if self.allowed_mentions is not None:
            data['allowed_mentions'] = self.allowed_mentions.to_json()
        if self.components is not None:
            data['components'] = list(map(lambda c: c.to_json(), self.components))

        return data


class InteractionResponse(JsonObject):
    type: InteractionCallbackType
    data: InteractionCallbackData

    @classmethod
    def from_dict(cls, data: JSON) -> 'InteractionResponse':
        return cls(
            type=InteractionCallbackType.from_value(data['type']),
            data=InteractionCallbackData.from_dict(data['data'])
        )

    def __init__(
            self,
            type: InteractionCallbackType,
            data: Optional[InteractionCallbackData] = None
    ) -> None:
        self.type = type
        self.data = data

    def to_dict(self) -> JSON:
        return {
            'type': self.type.value,
            'data': self.data.to_dict()
        }
