import glob
import json
import typing

import ollama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
import schemas

CFG = config.Config()

app = FastAPI(
    title=CFG.title,
    version=CFG.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CFG.trust_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/", tags=['inference'])
async def prompt(request: schemas.requests.Inference) -> schemas.Response:
    return schemas.Response(
        model=request.model,
        prompt=[
            schemas.requests.chat.Message(
                role='system',
                content=request.system
            ),
            schemas.requests.chat.Message(
                role='user',
                content=request.prompt
            )
        ],
        response=(
            ollama.generate(
                model=request.model,
                system=request.system,
                prompt=request.prompt
            )
            ['response']
        ),
        log_path=CFG.response_log_path
    )


@app.post("/chat/", tags=['inference'])
async def chat(request: schemas.requests.Chat) -> schemas.Response:
    return schemas.Response(
        model=request.model,
        prompt=request.messages,
        response=(
            ollama.chat(
                model=request.model,
                messages=[dict(message) for message in request.messages]
            )
            ['message']['content']
        ),
        log_path=CFG.response_log_path
    )


@app.post("/embed/", tags=['inference'])
async def embedding(request: schemas.requests.Embedding) -> schemas.Response:
    return schemas.Response(
        model=request.model,
        prompt=[
            schemas.requests.chat.Message(
                role='user',
                content=request.prompt
            )
        ],
        response=(
            ollama.embeddings(
                model=request.model,
                prompt=request.prompt
            )
            ['embedding']
        ),
        log_path=CFG.embedding_log_path
    )


@app.get("/embed/", tags=['data'])
async def get_embed() -> typing.List[dict]:
    return [
        json.load(open(path)) for path in
        glob.glob(f'{CFG.embedding_log_path}/*.json')
    ]


@app.post("/feedback/", tags=['annotate'])
async def feedback(request: schemas.requests.Feedback):
    request.log(CFG.feedback_log_path)
    return True


@app.get("/feedback/", tags=['data'])
async def get_feedback() -> typing.List[dict]:
    return [
        json.load(open(path)) for path in
        glob.glob(f'{CFG.feedback_log_path}/*.json')
    ]


@app.get("/models/", tags=['data'])
async def get_models() -> typing.List[schemas.Model]:
    return CFG.models


@app.get("/personas/", tags=['data'])
async def get_personas() -> typing.List[schemas.Persona]:
    return CFG.personas


@app.get("/responses/", tags=['data'])
async def get_responses() -> typing.List[dict]:
    return [
        json.load(open(path)) for path in
        glob.glob(f'{CFG.response_log_path}/*.json')
    ]
