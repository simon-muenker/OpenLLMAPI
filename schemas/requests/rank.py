import datetime
import json
import uuid

import pydantic


class Rank(pydantic.BaseModel):
    winner: uuid.UUID
    loser: uuid.UUID

    timestamp: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
