import typing

import pydantic


class _Request(pydantic.BaseModel):
    model: typing.Literal[
        "llama3.1:8b",
        "llama3.3:70b",
        "mistral:7b",
        "mistral-large:123b",
        "deepseek-r1:7b",
        "deepseek-r1:70b",
        "qwen2.5:7b",
        "qwen2.5:72b"
    ] = "llama3.1:8b"

    access_token: str | None = pydantic.Field(None, exclude=True)
    options: typing.Dict = pydantic.Field(default_factory=dict)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "llama3.1:8b",
                    "options": {}
                }
            ]
        }
    }


__all__ = ["_Request"]
