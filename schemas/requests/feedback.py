import datetime
import json
import typing
import uuid

import pydantic


class Feedback(pydantic.BaseModel):
    id: uuid.UUID
    content: typing.Literal['positive', 'negative']

    timestamp: datetime.datetime = None

    def __init__(self, **data):
        super().__init__(**data)

        if self.timestamp is None:
            self.timestamp = datetime.datetime.now()

    def log(self, path: str) -> None:
        json.dump(
            self.model_dump(mode='json'),
            open(f'{path}/{self.id}.{self.timestamp}.json', "w"),
            indent=4
        )

    @classmethod
    def load(cls, path: str) -> 'Feedback':
        return cls(**json.load(open(path)))
