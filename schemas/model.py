import typing
import json

import pydantic


class Model(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal['instruct', 'chat']
    params: str
    author: str
    origin: str
    more_link: str

    @classmethod
    def load(cls, path: str) -> 'Model':
        return cls(**json.load(open(path)))
