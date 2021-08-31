from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Final, Dict, List, Any, NoReturn
from volt.embed import Embed

# Configs

ElementsPerPage: Final[str] = 'ElementsPerPage'

# Metadata
MaxPageIndex: Final[str] = 'MaxPageIndex'

__all__ = (
    'PaginatorException',
    'LastPageException',
    'FirstPageException',
    'AbstractPaginator',
    'FieldPaginator',
    'FullEmbedPaginator'
)


class PaginatorException(Exception):
    """Base class for paginator errors"""
    msg: str

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return f'{self.__class__.__name__} : {self.msg}'


class LastPageException(PaginatorException):
    def __init__(self):
        super(LastPageException, self).__init__('Paginator reached max page index. Cannot load next page.')


class FirstPageException(PaginatorException):
    def __init__(self):
        super(FirstPageException, self).__init__('Paginator reached first page index. Cannot load previous page.')


class NotEnoughElements(PaginatorException):
    def __init__(self):
        super(NotEnoughElements, self).__init__('Paginator does not have any elements! Cannot load page.')


PAGINATION_EMOJI: Dict[str, str] = {
    'first': '⏮️',
    'prev': '◀️',
    'next': '▶️',
    'last': '⏭️',
    'detach': '❌'
}


class AbstractPaginator(ABC):
    __message__: discord.Message
    elements: list

    @abstractmethod
    def add_element(self, element) -> AbstractPaginator:    ...

    @abstractmethod
    def load_page(self):    ...

    @abstractmethod
    async def previous_page(self):    ...

    @abstractmethod
    async def next_page(self):    ...

    @abstractmethod
    async def first_page(self):    ...

    @abstractmethod
    async def last_page(self):    ...

    @abstractmethod
    async def send_paginator(self, channel: discord.TextChannel, bot):    ...

    @abstractmethod
    async def handle_pagination(self, payload: discord.RawReactionActionEvent): ...

    def attach(self, bot):
        bot.logger.debug(
            f'Attaching handler for paginator(msg={self.__message__.id})'
        )
        bot.paginator_listeners.update({self.__message__.id: self.handle_pagination})

    async def detach(self, bot):
        bot.logger.debug(
            f'Detaching handler for paginator(msg={self.__message__.id})'
        )
        bot.paginator_listeners.pop(self.__message__.id)
        await self.__message__.clear_reactions()

    @property
    def element_count(self) -> int:
        return len(self.elements)


class FieldPaginator(AbstractPaginator):
    def __init__(
            self,
            title: str,
            description: str,
            colour: discord.Colour = discord.Colour.blurple(),
            image_url: str = None,
            thumbnail_url: str = None,
            author: Dict[str, str] = None,
            footer: Dict[str, str] = None
    ):
        self.elements: List[Dict[str, Any]] = []
        self.page_index: int = 1

        self.config = {
            ElementsPerPage: 5
        }

        self.meta = {
            MaxPageIndex: 0
        }

        self.embed = discord.Embed(title=title, description=description, colour=colour)
        if image_url:
            self.embed.set_image(url=image_url)
        if thumbnail_url:
            self.embed.set_thumbnail(url=thumbnail_url)
        if author:
            self.embed.set_author(**author)
        if footer:
            self.embed.set_footer(**footer)
        self.__message__: discord.Message = None

    def configurate(self, **kwargs):
        """
        Configurate Paginator.
        Kwargs:
            ElementsPerPage (int): Elements to show in single page.
        """
        self.config.update(**kwargs)

    def update_meta(self):
        element_count: int = len(self.elements)

        full_elem_pages: int = element_count // self.config[ElementsPerPage]
        remains_elem_page: int = 1 if element_count % self.config[ElementsPerPage] > 0 else 0
        required_pages: int = full_elem_pages + remains_elem_page
        self.meta[MaxPageIndex] = required_pages

    def add_element(self, name: str, value: str, inline: bool = False) -> FieldPaginator:
        self.elements.append({'name': name, 'value': value, 'inline': inline})
        self.update_meta()
        return self     # For method chaining.

    def load_page(self):
        self.embed.clear_fields()

        for element in self.elements[self.config[ElementsPerPage]*(self.page_index-1):self.config[ElementsPerPage]*self.page_index]:
            self.embed.add_field(**element)

    async def previous_page(self) -> NoReturn:
        self.page_index -= 1
        if self.page_index < 1:
            raise FirstPageException()
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.embed)

    async def next_page(self):
        self.page_index += 1
        if self.page_index > self.meta[MaxPageIndex]:
            raise LastPageException()
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.embed)

    async def first_page(self):
        self.page_index = 1
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.embed)

    async def last_page(self):
        self.page_index = self.meta[MaxPageIndex]
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.embed)

    async def send_paginator(self, channel: discord.TextChannel):
        if len(self.embed.fields) == 0:
            self.embed.add_field(
                name='No items exists',
                value='Paginator has no items inside.',
                inline=False
            )
        self.__message__: discord.Message = await channel.send(embed=self.embed)

    async def handle_pagination(self, payload: discord.RawReactionActionEvent):
        raise NotImplemented()


class FullEmbedPaginator(AbstractPaginator):
    def __init__(
            self,
            elements: List[discord.Embed] = None
    ):
        self.elements: List[discord.Embed] = elements or []
        self.page_index: int = 1

        self.cur_page: discord.Embed = self.elements[0] if len(self.elements) > 0 else None
        self.__message__: discord.Message = None

    def add_element(self, element: discord.Embed) -> FullEmbedPaginator:
        if not isinstance(element, discord.Embed):
            raise TypeError(f'FullEmbedPaginator receive `discord.Embed`, not `{type(element)}` as element!')

        self.elements.append(element)
        return self

    def load_page(self):
        try:
            self.cur_page: discord.Embed = self.elements[self.page_index-1]
        except IndexError:
            raise NotEnoughElements()

    async def previous_page(self) -> NoReturn:
        print(f'DEBUG: Paginator.prev() index update (before : {self.page_index}')
        self.page_index -= 1
        print(f'DEBUG: Paginator.prev() index update (after : {self.page_index}')
        if self.page_index < 1:
            print(f'DEBUG: Paginator.prev() index out of range. Reverting index change.')
            self.page_index += 1
            raise FirstPageException()
        print(f'Paginator > Loading previous page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def next_page(self) -> NoReturn:
        print(f'DEBUG: Paginator.next() index update (before : {self.page_index}')
        self.page_index += 1
        print(f'DEBUG: Paginator.next() index update (after : {self.page_index}')
        if self.page_index > len(self.elements):
            print(f'DEBUG: Paginator.next() index out of range. Reverting index change.')
            self.page_index -= 1
            raise LastPageException()
        print(f'Paginator > Loading next page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def first_page(self) -> NoReturn:
        self.page_index = 1
        print(f'Paginator > Loading first page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def last_page(self) -> NoReturn:
        self.page_index = self.element_count
        print(f'Paginator > Loading last page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def send_paginator(self, channel: discord.TextChannel, bot) -> NoReturn:
        self.load_page()
        self.__message__: discord.Message = await channel.send(embed=self.cur_page)
        for emoji in PAGINATION_EMOJI.values():
            await self.__message__.add_reaction(emoji)
        self.attach(bot)

    async def handle_pagination(self, bot, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == PAGINATION_EMOJI['prev']:
            try:
                await self.previous_page()
            except FirstPageException:
                msg: discord.Message = await bot.get_channel(payload.channel_id).send(embed=EmbedPresets.warn_embed(
                    title='더 이전의 페이지가 존재하지 않습니다!',
                    description='1페이지입니다.'
                ))
                await msg.delete(delay=3)
        elif payload.emoji.name == PAGINATION_EMOJI['next']:
            try:
                await self.next_page()
            except LastPageException:
                msg: discord.Message = await bot.get_channel(payload.channel_id).send(embed=EmbedPresets.warn_embed(
                    title='더 이후의 페이지가 존재하지 않습니다!',
                    description='마지막 페이지입니다.'
                ))
                await msg.delete(delay=3)
        elif payload.emoji.name == PAGINATION_EMOJI['first']:
            await self.first_page()
        elif payload.emoji.name == PAGINATION_EMOJI['last']:
            await self.last_page()
        elif payload.emoji.name == PAGINATION_EMOJI['detach']:
            await self.detach(bot)
        await self.__message__.remove_reaction(payload.emoji, payload.member)


class ButtonPaginator(AbstractPaginator):
    def __init__(
            self,
            elements: List[discord.Embed] = None
    ):
        self.elements: List[discord.Embed] = elements or []
        self.page_index: int = 1

        self.cur_page: discord.Embed = self.elements[0] if len(self.elements) > 0 else None
        self.__message__: discord.Message = None

    def add_element(self, element: discord.Embed) -> FullEmbedPaginator:
        if not isinstance(element, discord.Embed):
            raise TypeError(f'FullEmbedPaginator receive `discord.Embed`, not `{type(element)}` as element!')

        self.elements.append(element)
        return self

    def load_page(self):
        try:
            self.cur_page: discord.Embed = self.elements[self.page_index - 1]
        except IndexError:
            raise NotEnoughElements()

    async def previous_page(self) -> NoReturn:
        print(f'DEBUG: Paginator.prev() index update (before : {self.page_index}')
        self.page_index -= 1
        print(f'DEBUG: Paginator.prev() index update (after : {self.page_index}')
        if self.page_index < 1:
            print(f'DEBUG: Paginator.prev() index out of range. Reverting index change.')
            self.page_index += 1
            raise FirstPageException()
        print(f'Paginator > Loading previous page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def next_page(self) -> NoReturn:
        print(f'DEBUG: Paginator.next() index update (before : {self.page_index}')
        self.page_index += 1
        print(f'DEBUG: Paginator.next() index update (after : {self.page_index}')
        if self.page_index > len(self.elements):
            print(f'DEBUG: Paginator.next() index out of range. Reverting index change.')
            self.page_index -= 1
            raise LastPageException()
        print(f'Paginator > Loading next page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def first_page(self) -> NoReturn:
        self.page_index = 1
        print(f'Paginator > Loading first page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    async def last_page(self) -> NoReturn:
        self.page_index = self.element_count
        print(f'Paginator > Loading last page: index {self.page_index}, max_index {self.element_count}...')
        self.load_page()
        if self.__message__:
            await self.__message__.edit(embed=self.cur_page)

    def attach(self, bot):
        bot.interaction_paginators.update({self.__message__.id: self.handle_pagination})

    async def send_paginator(self, channel: discord.TextChannel, bot):
        self.load_page()
        self.__message__: discord.Message = await channel.send(embed=self.cur_page)
        # TODO : Add buttons instead.
        self.attach(bot)

    async def handle_pagination(self, interaction):
        # TODO : Write logic using discord/interactions endpoint!
        pass