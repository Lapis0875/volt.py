from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional, Final, List, Union, Dict
from plum import dispatch

from .abc import JsonObject
from .color import Color
from .types.type_hint import JSON


__all__ = (
    'Embed',
    'EmbedType',
    'EmbedImage',
    'EmbedVideo',
    'EmbedAuthor',
    'EmbedFooter',
    'EmbedProvider',
    'EmbedField',
    'TITLE_LIMIT',
    'DESCRIPTION_LIMIT',
    'AUTHOR_NAME_LIMIT',
    'FOOTER_TEXT_LIMIT',
    'FIELDS_LIMIT',
    'FIELD_NAME_LIMIT',
    'FIELD_VALUE_LIMIT'
)


EMBED_DICT_TYPE = Dict[str, Union[str, bool]]


# Embed Limits
TITLE_LIMIT: Final[int] = 256
DESCRIPTION_LIMIT: Final[int] = 4096
FIELDS_LIMIT: Final[int] = 25
FIELD_NAME_LIMIT: Final[int] = 256
FIELD_VALUE_LIMIT: Final[int] = 1024
FOOTER_TEXT_LIMIT: Final[int] = 2048
AUTHOR_NAME_LIMIT: Final[int] = 256


class EmbedType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    Rich = auto()
    Image = auto()
    Video = auto()
    GIFV = auto()
    Article = auto()
    Link = auto()


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
    url: Optional[str]          # source url of video
    proxy_url: Optional[str]    # a proxied url of the video
    height: Optional[int]       # height of video
    width: Optional[int]        # width of video

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
            EmbedType(data['title']) if 'title' in data else None,
            data.get('description'),
            data.get('url'),
            datetime.fromisoformat(data.get('timestamp')),
            Color(data.get('color'))

        )

    def __init__(
            self,
            title: Optional[str] = None,
            type: Optional[EmbedType] = None,
            description: Optional[str] = None,
            url: Optional[str] = None,
            timestamp: Optional[datetime] = None,
            color: Optional[Color] = None,
            footer: Optional[EmbedFooter] = None,
            image: Optional[EmbedImage] = None,
            thumbnail: Optional[EmbedImage] = None,
            video: Optional[EmbedVideo] = None,
            provider: Optional[EmbedProvider] = None,
            author: Optional[EmbedAuthor] = None,
            fields: Optional[List[EmbedField]] = None
    ):
        if length := len(title) > TITLE_LIMIT:
            raise ValueError(f'Embed.title can have up to {TITLE_LIMIT} characters, but you have {length} characters!')
        self.title = title
        self.type = type
        if length := len(description) > DESCRIPTION_LIMIT:
            raise ValueError(f'Embed.description can have up to {DESCRIPTION_LIMIT} characters, but you have {length} characters!')
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields

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

    @dispatch
    def add_field(self, field: EmbedField):
        if self.fields is None:
            self.fields = []
        self.fields.append(field)

    @dispatch
    def add_field(self, field: EMBED_DICT_TYPE):
        if self.fields is None:
            self.fields = []
        self.fields.append(EmbedField(**field))

    @dispatch
    def add_field(self, name: str, value: str, inline: Optional[bool] = None):
        if self.fields is None:
            self.fields = []
        self.fields.append(EmbedField(name, value, inline))

    def remove_field_at(self, index: int):
        if self.fields:
            self.fields.pop(index)

    @dispatch
    def remove_field(self, field: EmbedField):
        if self.fields:
            self.fields.remove(field)

    @dispatch
    def remove_field(self, field: EMBED_DICT_TYPE):
        if self.fields:
            self.fields.remove(EmbedField(**field))

    def insert_field(self, field: EmbedField, index: int = None):
        index = index or len(self.fields)
        self.fields.insert(index, field)

