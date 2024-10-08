import typing
import uuid
import logging

import ollama
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

import config
import schemas
import util

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
    response: schemas.Response = schemas.Response(
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
        response=ollama.generate(**request.model_dump())['response']
    )
    util.pydantic_to_json(f'{CFG.response_log_path}/{response.id}', response)
    return response


@app.post("/chat/", tags=['inference'])
async def chat(request: schemas.requests.Chat) -> schemas.Response:
    logging.warn(request.model_dump())
    response: schemas.Response = schemas.Response(
        model=request.model,
        prompt=request.messages,
        response=ollama.chat(**request.model_dump())['message']['content']
    )
    util.pydantic_to_json(f'{CFG.response_log_path}/{response.id}', response)
    return response


@app.post("/embed/", tags=['inference'])
async def embedding(request: schemas.requests.Embedding) -> schemas.Response:
    response: schemas.Response = schemas.Response(
        model="mxbai-embed-large",
        prompt=[
            schemas.requests.chat.Message(
                role='user',
                content=request.prompt
            )
        ],
        response=(
            ollama.embeddings(
                model="mxbai-embed-large",
                prompt=request.prompt
            )
            ['embedding']
        )
    )
    util.pydantic_to_json(f'{CFG.embedding_log_path}/{response.id}', response)
    return response


@app.get("/embed/", tags=['data'])
async def get_embeddings() -> typing.List[schemas.Response]:
    return util.pydantic_from_glob(
        f'{CFG.embedding_log_path}/*.json',
        schemas.Response
    )


@app.post("/feedback/", tags=['annotate'])
async def feedback(request: schemas.requests.Feedback) -> bool:
    util.pydantic_to_json(f'{CFG.feedback_log_path}/{request.id}', request)
    return True


@app.get("/feedback/", tags=['annotate'])
async def get_feedback() -> typing.List[schemas.requests.Feedback]:
    return util.pydantic_from_glob(
        f'{CFG.feedback_log_path}/*.json',
        schemas.requests.Feedback
    )


@app.post("/rank/", tags=['annotate'])
async def rank(request: schemas.requests.Rank) -> bool:
    util.pydantic_to_json(f'{CFG.rank_log_path}/{request.winner}', request)
    return True


@app.get("/rank/", tags=['annotate'])
async def get_ranks() -> typing.List[schemas.requests.Rank]:
    return util.pydantic_from_glob(
        f'{CFG.rank_log_path}/*.json',
        schemas.requests.Rank
    )


@app.get("/models/", tags=['data'])
async def get_models() -> typing.List[schemas.Model]:
    return CFG.models


@app.get("/personas/", tags=['data'])
async def get_personas() -> typing.List[schemas.Persona]:
    return CFG.personas


@app.get("/responses/", tags=['data'])
async def get_responses() -> typing.List[schemas.Response]:
    return util.pydantic_from_glob(
        f'{CFG.response_log_path}/*.json',
        schemas.Response
    )


@app.get("/responses/{idx}", tags=['data'])
async def get_response_by_id(idx: uuid.UUID) -> schemas.Response:
    item: typing.List[schemas.Response] = util.pydantic_from_glob(
        f'{CFG.response_log_path}/{idx}.json', schemas.Response
    )

    if not item:
        raise HTTPException(status_code=404, detail="Response not found")

    return item[0]
