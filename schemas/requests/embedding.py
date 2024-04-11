from ._request import _Request


class Embedding(_Request):
    prompt: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    **_Request.model_config['json_schema_extra']['examples'][0],
                    "prompt": "What is the meaning of life?",
                }
            ]
        }
    }
