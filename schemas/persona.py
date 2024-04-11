import typing

import pydantic


class Persona(pydantic.BaseModel):
    id: str
    name: str
    icon: str
    type: typing.List[typing.Literal['assistant']]
    description: str
    prompt: str
