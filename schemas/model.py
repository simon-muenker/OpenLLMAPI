import typing

import pydantic


class Model(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal['instruct', 'chat']
    params: str
    author: str
    origin: str
    more_link: str

    def __lt__(self, other: "Model"):
         return self.name < other.name