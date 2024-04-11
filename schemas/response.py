import datetime
import typing
import uuid

import pydantic

from . import requests


class Response(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid1)
    timestamp: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)

    model: str
    prompt: typing.List[requests.chat.Message]
    response: str | typing.List[float]
