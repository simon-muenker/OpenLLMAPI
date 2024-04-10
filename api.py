import typing
import json

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


@app.post("/")
async def inference(request: schemas.requests.Inference) -> schemas.Response:
    return schemas.Response(
        model=request.model,
        prompt=request.prompt,
        response=(
            ollama.generate(
                model=request.model,
                prompt=request.prompt
            )
            ['message']
            ['content']
        ),
        log_path=CFG.response_log_path
    )


@app.post("/chat/")
async def chat(request: schemas.requests.Chat) -> schemas.Response:
    return schemas.Response(
        model=request.model,
        prompt=request.prompt,
        response=(
            ollama.chat(model=request.model, messages=request.prompt)
            ['message']['content']
        ),
        log_path=CFG.response_log_path
    )


@app.post("/feedback/")
async def feedback(request: schemas.requests.Feedback):
    json.dump(
        request.model_dump(mode='json'),
        open(f'{CFG.feedback_log_path}/{request.id}.json', "w"),
        indent=4
    )
    return True


@app.get("/models/")
async def get_models() -> typing.List[schemas.Model]:
    return CFG.models


@app.get("/personas/")
async def get_personas() -> typing.List[schemas.Persona]:
    return CFG.personas
