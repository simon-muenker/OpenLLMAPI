import typing

import pydantic


class _Request(pydantic.BaseModel):
    model: typing.Literal[
        "llama3.1:8b-instruct-q6_K",
        "llama3.1:70b-instruct-q6_K",
        "llama3.3:70b-instruct-q6_K",
        "mistral:7b-instruct-v0.2-q6_K",
        "mixtral:8x7b-instruct-v0.1-q6_K",
        "phi3:14b-medium-128k-instruct-q6_K",
        "phi3.5:3.8b-mini-instruct-q6_K",
        "gemma:7b-instruct-q6_K",
        "gemma2:27b-instruct-q6_K",
        "qwen2:72b-instruct-q6_K",
    ] = "llama3.1:8b-instruct-q6_K"

    options: typing.Dict = pydantic.Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "llama3.1:8b-instruct-q6_K",
                    "options": {}
                }
            ]
        }
    }
