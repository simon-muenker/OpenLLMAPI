import typing
import pathlib
import datetime
import json
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pydantic

import ollama


class Config:
    title: str = 'University Trier CL - Inference API'
    version: str = '0.0.1'

    trust_origins: typing.List[str] = [
        'http://localhost:5173',
        'http://localhost:8000',
        'https://demo.twon.uni-trier.de',
        'https://bishop.xciv.de',
        'https://chat.sci.xciv.de'
    ]


    log_path: str = './logs'

    def __init__(self) -> None:
        self.log_path = f'{self.log_path}/{self.version}'
        pathlib.Path(self.log_path).mkdir(parents=True, exist_ok=True)


cfg = Config()

app = FastAPI(
    title=cfg.title,
    version=cfg.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.trust_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Request(pydantic.BaseModel):

    model: typing.Literal[
        'falcon:40b-instruct-q5_1',
        'gemma:7b-instruct-q6_K',
        'llama2:70b-chat-q6_K', 
        'mistral:7b-instruct-v0.2-q6_K', 
        'mixtral:8x7b-instruct-v0.1-q6_K',
        'qwen:72b-chat-v1.5-q6_K',
        ] = 'mixtral:8x7b-instruct-v0.1-q6_K'

    prompt: str


class Response(pydantic.BaseModel):
    id: uuid.UUID = None
    timestamp: datetime.datetime = None

    model: str
    prompt: str
    response: str


    def __init__(self, log_path: str = None, **data):
        super().__init__(**data)

        self.id = uuid.uuid1()
        self.timestamp = datetime.datetime.now()

        if log_path:
            self.log(log_path)

    def log(self, path: str) -> None:
        json.dump(
            self.model_dump(mode='json', exclude=set('log_path')),
            open(f'{path}/{self.id}.json', "w"),
            indent=4
        )


def local_inference(model: str, prompt: str) -> str:
    return (
                ollama
                .chat(
                    model=model,
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt,
                        },
                    ]
                )
                ['message']
                ['content']
            )


@app.post("/")
async def inference(request: Request) -> Response:
    return Response(
            model=request.model,
            prompt=request.prompt,
            response=local_inference(request.model, request.prompt),
            log_path=cfg.log_path
        )


