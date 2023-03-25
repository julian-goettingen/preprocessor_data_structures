import jinja2
import re
from parse_err import PPDSParseError
import config

import json
from json import JSONDecodeError

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
        json_args = re.search(CONSTRUCTOR_GETTER_REX, source_string).group(1)
    except:
        raise PPDSParseError(
            "Failed to extract PPDS_CONSTRUCTORS definition from header-file."
        )

    try:
        raw_constructors = json.loads(json_args)
    except JSONDecodeError as e:
        # todo: highlight problematic character with: \n{e.doc[e.pos]}
        raise PPDSParseError(
            f"Constructors found in header file, but it is not valid json. Args found: \n{json_args}\n\n Problem: \n{e}\n"
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


def get_args_from_source_string(source_string):

    try:
        json_args = re.search(ARGS_GETTER_REX, source_string).group(1)
    except:
        raise PPDSParseError("Failed to extract PPDS_ARGS definition from header-file.")

    try:
        raw_args = json.loads(json_args)
    except JSONDecodeError as e:
        # todo: highlight problematic character with: \n{e.doc[e.pos]}
        raise PPDSParseError(
            f"Args found in header file, but it is not valid json. Args found: \n{json_args}\n\n Problem: \n{e}\n"
        )

    if not isinstance(raw_args, dict):
        raise PPDSParseError(
            f"ARGS must be valid dictionary, but found {raw_args} of type {type}"
        )

    expect_keys = {"args", "kwargs"}
    if set(raw_args.keys()) != expect_keys:
        raise PPDSParseError(
            f"invalid PPDS_ARGS, keys must be {expect_keys} but are {raw_args.keys()}.\nFull args:\n{raw_args}"
        )

    args = list(raw_args["args"])
    kwargs = dict(raw_args["kwargs"])

    return args, kwargs


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
