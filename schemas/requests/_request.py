import typing

import pydantic


class _Request(pydantic.BaseModel):
    model: typing.Literal[
        'gemma:7b-instruct-q6_K',
        "gemma2:27b-instruct-q6_K",
        "llama3.1:8b-instruct-q6_K",
        "llama3.1:70b-instruct-q6_K",
        'mistral:7b-instruct-v0.3-q6_K',
        "mistral-large:123b-instruct-2407-q6_K",
        'mixtral:8x7b-instruct-v0.1-q6_K',
        'mixtral:8x22b-instruct-v0.1-q6_K',
        "phi3:14b-medium-128k-instruct-q6_K",
        'qwen2:72b-instruct-q6_K',
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
