import typing

import pydantic


class _Request(pydantic.BaseModel):
    model: typing.Literal[
        'falcon:40b-instruct-q5_1',
        'gemma:7b-instruct-q6_K',
        'llama2:70b-chat-q6_K',
        'llama3:70b-instruct-q6_K',
        'mistral:7b-instruct-v0.2-q6_K',
        'mixtral:8x7b-instruct-v0.1-q6_K',
        'qwen:72b-chat-v1.5-q6_K',
    ] = 'mixtral:8x7b-instruct-v0.1-q6_K'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "mixtral:8x7b-instruct-v0.1-q6_K",
                }
            ]
        }
    }
