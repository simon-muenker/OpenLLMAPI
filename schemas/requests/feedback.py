import json
import typing
import uuid

import pydantic


class Feedback(pydantic.BaseModel):
    id: uuid.UUID
    content: typing.Literal['positive', 'negative']
