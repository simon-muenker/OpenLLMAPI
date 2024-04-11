import glob
import pathlib
import typing

import schemas


class Config:
    title: str = 'OpenLLMAPI - University Trier CL'
    version: str = '0.2.0'

    trust_origins: typing.List[str] = [
        'http://localhost:5173',
        'http://localhost:8000',
        'https://demo.twon.uni-trier.de',
        'https://chat.cl.uni-trier.de',
        'https://bishop.xciv.de',
        'https://chat.sci.xciv.de'
    ]

    data_path: str = './data'
    log_path: str = './logs'

    def __init__(self) -> None:
        self.log_path = f'{self.log_path}/{self.version}'

        self.response_log_path = f'{self.log_path}/response'
        self.embedding_log_path = f'{self.log_path}/embedding'
        self.feedback_log_path = f'{self.log_path}/feedback'

        pathlib.Path(self.response_log_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.embedding_log_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.feedback_log_path).mkdir(parents=True, exist_ok=True)

        self.models: typing.List[schemas.Model] = [
            schemas.Model.load(model_path) for model_path
            in glob.glob(f'{self.data_path}/models/*.json')
        ]

        self.personas: typing.List[schemas.Persona] = [
            schemas.Persona.load(persona_path) for persona_path
            in glob.glob(f'{self.data_path}/personas/*.json')
        ]
