import typing
import uuid
import logging

import ollama
from fastapi import FastAPI, HTTPException, Request
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


def check_permission(request: Request) -> None:
    try:
        if request.headers['origin'] in CFG.allowed_websites:
            return
    
    except KeyError:
        if request.headers["x-forwarded-for"] in CFG.ip_blacklist:
                logging.warning(f"Permission denied for IP: {request.headers['x-forwarded-for']}")
                raise HTTPException(status_code=403, detail="Permission denied. You are blacklisted. Contact the administrator.")
    


@app.post("/", tags=['inference'])
async def prompt(request: schemas.requests.Inference, meta: Request) -> schemas.Response:
    check_permission(meta)

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
    return response


@app.post("/chat/", tags=['inference'])
async def chat(request: schemas.requests.Chat, meta: Request) -> schemas.Response:
    check_permission(meta)

    response: schemas.Response = schemas.Response(
        model=request.model,
        prompt=request.messages,
        response=ollama.chat(**request.model_dump())['message']['content']
    )
    return response


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
