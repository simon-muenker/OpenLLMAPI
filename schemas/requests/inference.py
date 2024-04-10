from ._request import _Request


class Inference(_Request):
    prompt: str
    system: str = ''

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    **_Request.model_config['json_schema_extra']['examples'][0],
                    "system": "You are a helpful assistant.",
                    "prompt": "What is the meaning of life?",
                }
            ]
        }
    }
