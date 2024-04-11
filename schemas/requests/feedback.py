import json
import typing
import uuid

import pydantic


class Feedback(pydantic.BaseModel):
    id: uuid.UUID
    content: typing.Literal['positive', 'negative']

    @classmethod
    def load(cls, path: str) -> 'Feedback':
        return cls(**json.load(open(path)))
