import typing
import uuid

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
        response=(
            ollama.generate(
                model=request.model,
                system=request.system,
                prompt=request.prompt
            )
            ['response']
        )
    )
    util.pydantic_to_json(f'{CFG.response_log_path}/{response.id}', response)
    return response


@app.post("/chat/", tags=['inference'])
async def chat(request: schemas.requests.Chat) -> schemas.Response:
    response: schemas.Response = schemas.Response(
        model=request.model,
        prompt=request.messages,
        response=(
            ollama.chat(
                model=request.model,
                messages=[dict(message) for message in request.messages]
            )
            ['message']['content']
        )
    )
    util.pydantic_to_json(f'{CFG.response_log_path}/{response.id}', response)
    return response


@app.post("/embed/", tags=['inference'])
async def embedding(request: schemas.requests.Embedding) -> schemas.Response:
    response: schemas.Response = schemas.Response(
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
async def update_item(idx: uuid.UUID) -> schemas.Response:
    item: typing.List[schemas.Response] = util.pydantic_from_glob(
        f'{CFG.response_log_path}/{idx}', schemas.Response
    )

    if not item:
        raise HTTPException(status_code=404, detail="Response not found")

    return item[0]
