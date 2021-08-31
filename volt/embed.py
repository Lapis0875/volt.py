from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import NamedTuple, Optional, Final, List

from .abc import JsonObject
from .color import Color
from .types.type_hint import JSON


# Embed Limits
TITLE_LIMIT: Final[int] = 256
DESCRIPTION_LIMIT: Final[int] = 4096
FIELDS_LIMIT: Final[int] = 25
FIELD_NAME_LIMIT: Final[int] = 256
FIELD_VALUE_LIMIT: Final[int] = 1024
FOOTER_TEXT_LIMIT: Final[int] = 2048
AUTHOR_NAME_LIMIT: Final[int] = 256


class EmbedType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    Rich = auto()
    Image = auto()
    Video = auto()
    GIFV = auto()
    Article = auto()
    Link = auto()

    @classmethod
    def from_value(cls, value: str) -> 'EmbedType':
        m = next(filter(lambda m: m.value == value, cls.__members__.values()), None)
        if m:
            return m
        else:
            raise ValueError(f'Embed Type with value {value} does not exist!')


@dataclass(init=True, eq=True, repr=True)
class EmbedImage(JsonObject):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]

    @classmethod
    def from_json(cls, data: JSON) -> 'EmbedImage':
        return cls(url=data.get('url'), proxy_url=data.get('proxy_url'), height=data.get('height'), width=data.get('width'))

    def to_json(self) -> JSON:
        data = {}
        if self.url:
            data['url'] = self.url
        if self.proxy_url:
            data['proxy_url'] = self.proxy_url
        if self.height:
            data['height'] = self.height
        if self.width:
            data['width'] = self.width
        return data


@dataclass(init=True, eq=True, repr=True)
class EmbedVideo(JsonObject):
    url: Optional[str]      # source url of video
    proxy_url: Optional[str]    # a proxied url of the video
    height: Optional[int]   # height of video
    width: Optional[int]    # width of video

    @classmethod
    def from_json(cls, data: JSON) -> 'EmbedVideo':
        return cls(url=data.get('url'), proxy_url=data.get('proxy_url'), height=data.get('height'), width=data.get('width'))

    def to_json(self) -> JSON:
        data = {}
        if self.url:
            data['url'] = self.url
        if self.proxy_url:
            data['proxy_url'] = self.proxy_url
        if self.height:
            data['height'] = self.height
        if self.width:
            data['width'] = self.width
        return data


@dataclass(init=True, eq=True, repr=True)
class EmbedProvider(JsonObject):
    name: Optional[str]
    url: Optional[str]

    @classmethod
    def from_json(cls, data: JSON) -> 'EmbedProvider':
        return cls(data.get('name'), data.get('url'))

    def to_json(self) -> JSON:
        data = {}
        if self.name:
            data['name'] = self.name
        if self.url:
            data['url'] = self.url
        return data


@dataclass(init=False, eq=True, repr=True)
class EmbedAuthor(JsonObject):
    """
    Embed Author Object.
    """

    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]

    @classmethod
    def from_json(cls, data: JSON) -> 'EmbedAuthor':
        return cls(
            name=data.get('name'),
            url=data.get('url'),
            icon_url=data.get('icon_url'),
            proxy_icon_url=data.get('proxy_icon_url')
        )

    def __init__(self, name: Optional[str] = None, url: Optional[str] = None, icon_url: Optional[str] = None, proxy_icon_url: Optional[str] = None):
        if name is not None and (length := len(name) > AUTHOR_NAME_LIMIT):
            raise ValueError(f'Embed.author.name can have up to {AUTHOR_NAME_LIMIT} characters, but you have {length}!')

    def to_json(self) -> JSON:
        data = {}
        if self.name:
            data['name'] = self.name
        if self.url:
            data['url'] = self.url
        if self.icon_url:
            data['icon_url'] = self.icon_url
        if self.proxy_icon_url:
            data['proxy_icon_url'] = self.proxy_icon_url
        return data


@dataclass(init=False, eq=True, repr=True)
class EmbedFooter(JsonObject):
    text: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]

    @classmethod
    def from_json(cls, data: JSON) -> 'EmbedFooter':
        return cls(data.get('text'), data.get('icon_url'), data.get('proxy_icon_url'))

    def __init__(self, text: Optional[str] = None, icon_url: Optional[str] = None, proxy_icon_url: Optional[str] = None):
        if text is not None and (length := len(text) > FOOTER_TEXT_LIMIT):
            raise ValueError(f'Embed.footer.text can have up to {FOOTER_TEXT_LIMIT} characters, but you have {length}!')
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url

    def to_json(self) -> JSON:
        data = {}
        if self.text:
            data['text'] = self.text
        if self.icon_url:
            data['icon_url'] = self.icon_url
        if self.proxy_icon_url:
            data['proxy_icon_url'] = self.proxy_icon_url
        return data


@dataclass(init=False, eq=True, repr=True)
class EmbedField(JsonObject):
    name: str
    value: str
    inline: Optional[bool]

    @classmethod
    def from_json(cls, data: JSON) -> 'JsonObject':
        return cls(data['name'], data['value'], data.get('inline'))

    def __init__(self, name: str, value: str, inline: Optional[bool] = None):
        if length := len(name) > FIELD_NAME_LIMIT:
            raise ValueError(f'Embed.field.name can have up to {FIELD_NAME_LIMIT} characters, but you have {length} characters!')
        self.name = name
        if length := len(value) > FIELD_VALUE_LIMIT:
            raise ValueError(f'Embed.field.value can have up to {FIELD_VALUE_LIMIT} characters, but you have {length} characters!')
        self.value = value
        self.inline = inline

    def to_json(self) -> JSON:
        data = {
            'name': self.name,
            'value': self.value
        }
        if self.inline is not None:
            data['inline'] = self.inline
        return data


@dataclass(init=False, eq=True, repr=True)
class Embed(JsonObject):
    """
    discord embed object.
    """
    title: Optional[str]
    type: Optional[EmbedType]
    description: Optional[str]
    url: Optional[str]
    timestamp: datetime
    color: Optional[Color]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedImage]
    thumbnail: Optional[EmbedImage]
    video: Optional[EmbedVideo]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields: List[EmbedField]

    @classmethod
    def from_json(cls, data: JSON) -> 'JsonObject':
        return cls(
            data.get('title'),
            EmbedType.from_value(data['title']) if 'title' in data else None,
            data.get('description'),

        )

    def __init__(
            self,
            title: Optional[str],
            type: Optional[EmbedType],
            description: Optional[str],
    ):
        if length := len(title) > TITLE_LIMIT:
            raise ValueError(f'Embed.title can have up to {TITLE_LIMIT} characters, but you have {length} characters!')
        self.title = title
        self.type = type
        if length := len(description) > DESCRIPTION_LIMIT:
            raise ValueError(f'Embed.description can have up to {DESCRIPTION_LIMIT} characters, but you have {length} characters!')
        self.description = description
        # TODO : Fill __init__

    def to_json(self) -> JSON:
        data = {}
        if self.title:
            data.update(title=self.title)
        if self.type:
            data.update(type=self.type.value)
        if self.description:
            data.update(description=self.description)
        if self.url:
            data.update(url=self.url)
        if self.timestamp:
            data.update(timestamp=self.timestamp.isoformat())
        if self.color:
            data.update(color=self.color)
        if self.footer:
            data.update(footer=self.footer.to_json())
        if self.image:
            data.update(image=self.image.to_json())
        if self.thumbnail:
            data.update(thumbnail=self.thumbnail.to_json())
        if self.video:
            data.update(video=self.video.to_json())
        if self.provider:
            data.update(provider=self.provider.to_json())
        if self.author:
            data.update(author=self.author.to_json())
        if self.fields:
            data.update(fields=list(map(lambda f: f.to_json(), self.fields)))
        return data

