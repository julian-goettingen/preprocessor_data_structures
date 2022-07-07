import re
import jinja2
import json

from parse_err import PPDSParseError
from json import JSONDecodeError

# modified from:
# https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
# this preserves line numbers by inserting newlines
def remove_comments(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " + "\n"*s.count("\n")
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


# template_getter_rex = re.compile("/\*\s+PPDS_SOURCE\s+(.*?)\*/", re.MULTILINE|re.DOTALL)
# def get_template_from_source(source_filename):

#     with open(source_filename, "r") as f:
#         template = re.search(template_getter_rex, f.read())

#     return template.group(1)

# DEF_GETTER_REX = re.compile("/\*\s+PPDS_DEF:\s+(.*?)\*/", re.MULTILINE|re.DOTALL)
# UNDEF_GETTER_REX = re.compile("/\*\s+PPDS_UNDEF:\s+(.*?)\*/", re.MULTILINE|re.DOTALL)
# ARGS_GETTER_REX = re.compile("/\*\s+PPDS_ARGS:\s+(.*?)\*/", re.MULTILINE|re.DOTALL)

# # TODO: better error handling
# # idea: make line numbers in source-file match linenumbers in source_string
# def get_def_template_from_source_string(source_string):
#     template = re.search(DEF_GETTER_REX, source_string)
#     if not template:
#         # TODO: report close match?
#         raise PPDSParseError("Expected header-file to contain a DEF-template.")
#     try:
#         return jinja2.Template(template.group(1), undefined=jinja2.StrictUndefined)
#     except jinja2.exceptions.UndefinedError as e:
#         print(e)
#         print(e.__dict__)
#         raise PPDSParseError("header-file contains undefined:")

# use this environment for the other Template-instantiations too,
# then set the globals correctly to include the python-module and allow importing jinja-macros
# also: why are there four, not two Template?
# def get_undef_template_from_source_string(source_string):
#     template = re.search(UNDEF_GETTER_REX, source_string)
#     if not template:
#         raise PPDSParseError("Expected header-file to contain an UNDEF-template.")
#     try:
#         return env.from_string(template.group(1))
#     except jinja2.exceptions.UndefinedError as e:
#         print(e)
#         print(e.__dict__)
#         raise PPDSParseError("header-file contains undefined:")




# def get_args_from_source_string(source_string):

#     try: 
#         json_args = re.search(ARGS_GETTER_REX, source_string).group(1)
#     except:
#         raise PPDSParseError("Failed to extract PPDS_ARGS definition from header-file.")

#     try:
#         raw_args = json.loads(json_args)
#     except JSONDecodeError as e:
#         raise PPDSParseError(f"Args found in header file, but it is not valid json. Args found: \n{json_args}\n\n Problem: \n{e}")
    

#     assert isinstance(raw_args, dict)

#     expect_keys = {"args", "kwargs"}
#     if set(raw_args.keys()) != expect_keys:
#         raise PPDSParseError(f"invalid PPDS_ARGS, keys must be {expect_keys} but are {raw_args.keys()}.\nFull args:\n{raw_args}")

#     args = list(raw_args["args"])
#     kwargs = dict(raw_args["kwargs"])

#     return args, kwargs



def header_from_template(template_str, argdict, declare_site):
    try:
        return template_str.render(**argdict,declare_site=declare_site)+"\n\n"
    except jinja2.TemplateError as e:
        print(e)
        print(e.__dict__)
        raise PPDSParseError(f"{type(e).__name__} with message: {e.message}")