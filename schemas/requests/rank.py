import datetime
import json
import uuid

import pydantic


class Rank(pydantic.BaseModel):
    winner: uuid.UUID
    loser: uuid.UUID

    timestamp: datetime.datetime = None

    def __init__(self, **data):
        super().__init__(**data)

        self.timestamp = datetime.datetime.now()

    def log(self, path: str) -> None:
        json.dump(
            self.model_dump(mode='json'),
            open(f'{path}/{self.id}.{self.timestamp}.json', "w"),
            indent=4
        )
