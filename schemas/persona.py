import typing

import pydantic


class Persona(pydantic.BaseModel):
    id: str
    name: str
    icon: str
    type: typing.List[typing.Literal['assistant']]
    description: str
    prompt: str

    def __lt__(self, other: "Persona"):
        if self.name[0] == "_":
         return True

         return self.name < other.name