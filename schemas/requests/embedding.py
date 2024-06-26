import pydantic


class Embedding(pydantic.BaseModel):
    prompt: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "What is the meaning of life?",
                }
            ]
        }
    }
