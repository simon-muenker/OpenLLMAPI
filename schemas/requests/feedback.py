import datetime
import typing
import uuid

import pydantic


class Feedback(pydantic.BaseModel):
    id: uuid.UUID
    content: typing.Literal['positive', 'negative']

    timestamp: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
