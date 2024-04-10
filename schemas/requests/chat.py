import typing

import pydantic

from ._request import _Request


class Message(pydantic.BaseModel):
    role: typing.Literal['user', 'assistant', 'system']
    content: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "What is the meaning of life?",
                },
                {
                    "role": "assistant",
                    "content": "42",
                }
            ]
        }
    }


class Chat(_Request):
    messages: typing.List[Message]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    **_Request.model_config['json_schema_extra']['examples'][0],
                    "messages": Message.model_config['json_schema_extra']['examples'],
                }
            ]
        }
    }
