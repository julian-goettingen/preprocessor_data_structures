import re
import jinja2
import json


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


template_getter_rex = re.compile("/\*\s+PPDS_SOURCE\s+(.*?)\*/", re.MULTILINE|re.DOTALL)
def get_template_from_source(source_filename):

    with open(source_filename, "r") as f:
        template = re.search(template_getter_rex, f.read())

    return template.group(1)

DEF_GETTER_REX = re.compile("/\*\s+PPDS_DEF:\s+(.*?)\*/", re.MULTILINE|re.DOTALL)
UNDEF_GETTER_REX = re.compile("/\*\s+PPDS_UNDEF:\s+(.*?)\*/", re.MULTILINE|re.DOTALL)
ARGS_GETTER_REX = re.compile("/\*\s+PPDS_ARGS:\s+(.*?)\*/", re.MULTILINE|re.DOTALL)

# TODO: better error handling
# idea: make line numbers in source-file match linenumbers in source_string
def get_def_template_from_source_string(source_string):
    template = re.search(DEF_GETTER_REX, source_string)
    return jinja2.Template(template.group(1), undefined=jinja2.StrictUndefined)

def get_undef_template_from_source_string(source_string):
    template = re.search(UNDEF_GETTER_REX, source_string)
    return jinja2.Template(template.group(1), undefined=jinja2.StrictUndefined)

def get_args_from_source_string(source_string):
    raw_args = json.loads(re.search(ARGS_GETTER_REX, source_string).group(1))

    #TODO: better error messages
    err_msg = str(raw_args)+" is not valid as args"

    #validate
    if not isinstance(raw_args, dict):
        raise ValueError(err_msg)
    if set(raw_args.keys()) != {"args", "kwargs"}:
        raise ValueError(err_msg)

    args = list(raw_args["args"])
    kwargs = dict(raw_args["kwargs"])

    return args, kwargs




def split_smart(s):

    bracket_stack = []
    result_list = []
    current_str = []

    def finalize_arg():
        nonlocal current_str,result_list
        result_list.append("".join(current_str))
        current_str = []

    for c in s:
        if c == "," and len(bracket_stack)==0:
            finalize_arg()
            continue
        current_str.append(c)
        if c in "([{":
            bracket_stack.append(c)
        elif c in ")]}":
            t = bracket_stack.pop()
            if t != c:
                raise ValueError(s+" has invalid brackets")
    finalize_arg()

    return result_list

def preprocess_raw_args(raw_args):

    #only what is between the outermost brackets is an argument

    m = re.match(r"\((.*?)\)", raw_args)
    if not m:
        print("Syntax Error")
        exit(1)

    args = split_smart(m.groups()[0])
    return args


def header_from_template(template_str, argdict, declare_site):
    return template_str.render(**argdict,declare_site=declare_site)+"\n\n"
