import glob
import json
import typing


def load_from_path(
        path_pattern: str,
        loader: typing.Callable = lambda x: json.load(open(x))
) -> typing.List[typing.Any]:
    return [loader(path) for path in glob.glob(path_pattern)]
