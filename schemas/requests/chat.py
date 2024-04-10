import typing

import pydantic

from ._request import _Request


class Message(pydantic.BaseModel):
    role: typing.Literal['user', 'assistant', 'system']
    content: str


class Chat(_Request):
    messages: typing.List[Message]
