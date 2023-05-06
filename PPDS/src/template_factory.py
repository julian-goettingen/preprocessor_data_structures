from typing import Any, Tuple, List, Dict
from typeguard import check_type, TypeCheckError

import jinja2
import re
from parse_err import PPDSParseError
import config

import yaml
from yaml import YAMLError, MarkedYAMLError

import jinja_callable

_env = None


def get_env(local_get_config=config.get_config):
    global _env
    if _env is None:
        _env = jinja2.Environment(
            undefined=jinja2.StrictUndefined,
            loader=jinja2.FileSystemLoader(local_get_config().source_header_loc),
        )
        _env.globals["hello_python"] = jinja_callable.hello_python
    return _env


DEF_GETTER_REX = re.compile("/\*\s+PPDS_DEF:\s+(.*?)\*/", re.MULTILINE | re.DOTALL)
UNDEF_GETTER_REX = re.compile("/\*\s+PPDS_UNDEF:\s+(.*?)\*/", re.MULTILINE | re.DOTALL)
ARGS_GETTER_REX = re.compile("/\*\s+PPDS_ARGS:\s+(.*?)\*/", re.MULTILINE | re.DOTALL)
CONSTRUCTOR_GETTER_REX = re.compile(
    "/\*\s+PPDS_CONSTRUCTORS:\s+(.*?)\*/", re.MULTILINE | re.DOTALL
)
template_getter_rex = re.compile(
    "/\*\s+PPDS_SOURCE\s+(.*?)\*/", re.MULTILINE | re.DOTALL
)


def get_template_from_source(source_filename):

    with open(source_filename, "r") as f:
        template = re.search(template_getter_rex, f.read())

    return template.group(1)


def get_constructors_from_source_string(source_string):

    try:
        yaml_args = re.search(CONSTRUCTOR_GETTER_REX, source_string).group(1)
    except:
        raise PPDSParseError(
            "Failed to extract PPDS_CONSTRUCTORS definition from header-file."
        )

    try:
        raw_constructors = yaml.safe_load(yaml_args)
    except YAMLError as e:
        # todo: highlight problematic character with: \n{e.doc[e.pos]} <=== this was for json
        # similar thing possible for yaml?
        raise PPDSParseError(
            f"Constructors found in header file, but it is not valid yaml. Args found: \n{yaml_args}\n\n Problem: \n{e}\n"
        )

    if not isinstance(raw_constructors, list):
        raise PPDSParseError(
            f"ARGS must be valid list (json-format), but found {raw_constructors} of type {type}"
        )

    if not len(raw_constructors) > 0:
        raise PPDSParseError(f"need at least one constructor, found {raw_constructors}")

    constr_rexes = []
    for r in raw_constructors:
        try:
            cmpd = re.compile(r)
        except Exception as e:
            raise PPDSParseError(
                f"constructor must be valid python regex.\nFound:\n{r}\nProblem:\n{e}"
            )
        else:
            if cmpd.groups != 1:
                raise PPDSParseError(
                    f"constructors are expected to have one group to match the arguments, but found {cmpd.groups} in the following constructor:\n{r}"
                )
            else:
                constr_rexes.append(cmpd)

    assert len(constr_rexes) > 0

    return constr_rexes

def parse_yaml_args(yaml_args: str) -> Tuple[List[str], Dict[str, str]]:

    try:
        raw_args = yaml.safe_load(yaml_args)
    except YAMLError as e:
        # todo: highlight problematic character with: \n{e.doc[e.pos]} <== that was for json
        raise PPDSParseError(
            f"Args found in header file, but it is not validyaml. Args found: \n{yaml_args}\n\n Problem: \n{e}\n"
        )

    if not isinstance(raw_args, dict):
        raise PPDSParseError(
            f"ARGS must be valid dictionary, but {yaml_args} was decoded to {raw_args} of type {type(raw_args)}"
        )

    expect_keys = {"args", "kwargs"}
    if set(raw_args.keys()) != expect_keys:
        raise PPDSParseError(
            f"invalid PPDS_ARGS, keys must be {expect_keys} but are {raw_args.keys()}.\nFull args:\n{raw_args}"
        )

    args = list(raw_args["args"])
    kwargs = dict(raw_args["kwargs"])


    try:
        check_type(kwargs, Dict[str, str])
    except TypeCheckError as e:
        raise PPDSParseError(f"Found invalid keyword-arguments in source-file: {kwargs}\nkeys and values of mapping must be strings\nError: {e}")
    try:
        check_type(args, List[str])
    except TypeCheckError as e:
        raise PPDSParseError(f"Found invalid positional arguments in source-file: {args}\n must be a list of strings\nError: {e}")

    return args, kwargs

def get_args_from_source_string(source_string) -> Tuple[List[str], Dict[str, str]]:

    try:
        yaml_args = re.search(ARGS_GETTER_REX, source_string).group(1)
    except:
        raise PPDSParseError("Failed to extract PPDS_ARGS definition from header-file.")

    return parse_yaml_args(yaml_args)


def get_undef_template_from_source_string(source_string):
    template = re.search(UNDEF_GETTER_REX, source_string)
    if not template:
        raise PPDSParseError("Expected header-file to contain an UNDEF-template.")
    try:
        return get_env().from_string(template.group(1))
    except jinja2.exceptions.UndefinedError as e:
        print(e)
        print(e.__dict__)
        raise PPDSParseError("header-file contains undefined:")


# TODO: better error handling
# idea: make line numbers in source-file match linenumbers in source_string
def get_def_template_from_source_string(source_string):
    template = re.search(DEF_GETTER_REX, source_string)
    if not template:
        # TODO: report close match?
        raise PPDSParseError("Expected header-file to contain a DEF-template.")
    try:
        return get_env().from_string(template.group(1))
    except jinja2.exceptions.UndefinedError as e:
        print(e)
        print(e.__dict__)
        raise PPDSParseError("header-file contains undefined:")
