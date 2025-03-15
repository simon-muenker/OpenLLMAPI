import pathlib
import typing

import schemas
import util


class Config:
    title: str = 'OpenLLMAPI - University Trier CL'
    version: str = '0.3.1'

    trust_origins: typing.List[str] = ['*']

    data_path: str = './data'
    log_path: str = './logs'

    def __init__(self) -> None:
        self.log_path = f'{self.log_path}/{self.version}'

        self.feedback_log_path = f'{self.log_path}/feedback'
        self.rank_log_path = f'{self.log_path}/rank'

        pathlib.Path(self.feedback_log_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.rank_log_path).mkdir(parents=True, exist_ok=True)

        self.ip_blacklist: typing.List[str] = open(f"{self.data_path}/ip_blacklist.txt").read().splitlines()

        self.models: typing.List[schemas.Model] = sorted(
                util.pydantic_from_glob(
                f'{self.data_path}/models/*.json',
                schemas.Model
            )
        )

        self.personas: typing.List[schemas.Persona] = sorted(
            util.pydantic_from_glob(
                f'{self.data_path}/personas/*.json',
                schemas.Persona
            )
        )

    @property
    def allowed_websites(self) -> typing.List[str]:
        return open(f"{self.data_path}/allowed_websites.txt").read().splitlines()
