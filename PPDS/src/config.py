from dataclasses import dataclass
import json

from pydantic import ValidationError
from pydantic.dataclasses import dataclass
from typing import Union, Dict, List
import os

from requests import JSONDecodeError


@dataclass
class PPDSConfig:
    source_header_loc: str
    target_header_loc: str
    interface_desc_loc: str
    pygen_target_loc: str | None
    pygen_usables_loc: str | None
    search_paths: List[str]
    global_default_params: Dict[str, str]




def _ensure_valid_dir(config, name, allow_none=False):

    path = config[name]
    if path is None and allow_none:
        return

    if os.path.isdir(path):
        return

    if not os.path.isdir(path):
        print(f"config-file specifies a path for {name} that could not be found: {repr(path)}")
        print(f"if the path is right, you need to create the directory.")
        exit(1)


xpected_keys = {
    "source_header_loc",
    "target_header_loc",
    "interface_desc_loc",
    "search_paths",
    "global_default_params",
    "pygen_target_loc",
    "pygen_usables_loc",
}


def _read() -> PPDSConfig:

    # defaults
    config: Dict[str, Union[str, None]] = {"pygen_target_loc": None, "pygen_usables_loc": None}

    try:
        with open("./ppds_config.json", "r") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        print(
            "could not find config file, must be called `ppds_config.json` and be located at the root of the project (where the call to ppds should be made)"
        )
        exit(1)
    except JSONDecodeError as e:
        print("could not decode config-file. Reason: ", e)
        exit(1)

    for k in config:
        # numbers are converted to string (because all of ppds works with strings)
        config[k] = str(config[k]) if isinstance(config[k], (int, float)) else config[k]

    unknown_keys = set(config.keys()) - xpected_keys
    if len(unknown_keys) > 0:
        print(f"unknown elements in config file: {unknown_keys}")
        print(f"allowed keys are {xpected_keys}")
        exit(1)

    missing_keys = xpected_keys - set(config.keys())
    if len(missing_keys) > 0:
        print(f"config-file is missing keys: {missing_keys}")
        print(f"must include: {xpected_keys}")
        exit(1)

    _ensure_valid_dir(config, "source_header_loc")
    _ensure_valid_dir(config, "target_header_loc")
    _ensure_valid_dir(config, "interface_desc_loc")
    _ensure_valid_dir(config, "pygen_target_loc", allow_none=True)
    _ensure_valid_dir(config, "pygen_usables_loc", allow_none=True)

    if config["pygen_target_loc"] is not None and config["pygen_usables_loc"] is None:
        print(
            "need to set the location of the pygen_usables directory to use generated python code"
        )
        exit(1)

    if not isinstance(config["global_default_params"], dict):
        print(
            "global_default_param must be dict of (name, value), but found: ",
            repr(config["global_default_params"]),
            "of type",
            type(config["global_default_params"])
        )
        exit(1)

    if not isinstance(config["search_paths"], list):
        print(
            "search path must be a list of valid paths (can be a list with a single element, and can use glob-style matchers * and **)"
        )
        exit(1)

    try:
        res = PPDSConfig(**config)
        return res
    except ValidationError as e:
        print(f"""
        Config-file has validation-errors, see below:
        {e}
        """)
    except:
        print("failed to understand config-file. Reason: ", e)
        exit(1)


_config = None


def get_config() -> PPDSConfig:
    global _config
    if _config is None:
        _config = _read()
    return _config
