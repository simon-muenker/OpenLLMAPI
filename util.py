import glob
import json
import typing

import pydantic


def pydantic_from_glob(
        path_pattern: str,
        cls: typing.Callable
) -> typing.List[typing.Any]:
    return [cls(**json.load(open(path))) for path in glob.glob(path_pattern)]


def pydantic_to_json(path: str, model: pydantic.BaseModel) -> None:
    json.dump(
        model.model_dump(mode='json'),
        open(f'{path}.json', "w"),
        indent=4
    )
