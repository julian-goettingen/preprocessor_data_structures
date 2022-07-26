from dataclasses import dataclass
import json
from dataclasses import dataclass
from typing import Union
import os

from requests import JSONDecodeError

@dataclass
class PPDSConfig():
    source_header_loc: str
    target_header_loc: str
    interface_desc_loc: str
    search_paths: list[str]
    global_default_params: dict[str, Union[str,int]]


def _ensure_valid_dir(path):
    if not os.path.isdir(path):
        print(f"config-file specifies path that could not be found: {path}")
        exit(1)
    

def _read():

    try:
        with open("./ppds_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("could not find config file, must be called `ppds_config.json` and be located at the root of the project (where the call to ppds should be made)")
        exit(1)
    except JSONDecodeError as e:
        print("could not decode config-file. Reason: ", e)
        exit(1)
    
    xpected_keys = {"source_header_loc", "target_header_loc", "interface_desc_loc", "search_paths", "global_default_params"}
    unknown_keys = set(config.keys()) - xpected_keys
    if len(unknown_keys)>0:
        print(f"unknown elements in config file: {unknown_keys}")
        print(f"allowed keys are {xpected_keys}")
        exit(1)

    missing_keys = xpected_keys - set(config.keys())
    if len(missing_keys)>0:
        print(f"config-file is missing keys: {missing_keys}")
        print(f"must include: {xpected_keys}")
        exit(1)
    
    _ensure_valid_dir(config["source_header_loc"])
    _ensure_valid_dir(config["target_header_loc"])
    _ensure_valid_dir(config["interface_desc_loc"])

    if not isinstance(config["global_default_params"], dict):
        print("global_default_param must be dict of (name, value), but found: ", config["global_default_params"])
        exit(1)
    
    if not isinstance(config["search_paths"], list):
        print("search path must be a list of valid paths (can be a list with a single element, and can use glob-style matchers * and **)")
        exit(1)


    try:
        res = PPDSConfig(**config)
        return res
    except :
        print("failed to understand config-file. Reason: ", e)
        exit(1)


_config = None

def get_config():
    global _config
    if _config is None:
        _config = _read()
    return _config