import typing
import json

import pydantic


class Persona(pydantic.BaseModel):
    id: str
    name: str
    icon: str
    type: typing.List[typing.Literal['assistant']]
    description: str
    prompt: str

    @classmethod
    def load(cls, path: str) -> 'Persona':
        return cls(**json.load(open(path)))
