import re
from parse_err import PPDSParseError


def parse_args_string(raw_args, posarglist, kwargnames):

    arglist = preprocess_raw_args(raw_args)

    if len(arglist) < len(posarglist):
        raise PPDSParseError("Not enough positional arguments", detail=f"arglist {arglist} of length {len(arglist)} cannot satisfy required {len(posarglist)} positional arguments {posarglist}")


    argdict = {}

    argnum = 0
    # do positional arguments first
    for arg, argname in zip(arglist, posarglist):

        val = extract_valid_pos_arg(arg)
        argdict[argname] = val
        argnum += 1 # deliberately at bottom

    # iterate through the rest of arglist to get the keyword-args
    for arg in arglist[argnum:]:
        argname, val = extract_valid_kw_arg(arg)
        if argname not in kwargnames:
            raise PPDSParseError(f"{argname} is not a valid keyword-argument. Must be one of {kwargnames}")
        argdict[argname] = val
    
    return argdict


def preprocess_raw_args(raw_args):

    #only what is between the outermost brackets is an argument
    #remove everything except the stuff between them
    

    # todo: all of this should be handled by grammars not regexp
    m = re.match(r"\((.*)\)", raw_args)
    if not m:
        raise PPDSParseError("failed to parse arguments")

    args = split_smart(m.groups()[0])
    return args


# TODO: handle ==comparison and possibly even =assignment in brackets
# both this function and the one for keywords dont allow == sign in values
def extract_valid_pos_arg(s):

    if "=" in s and "==" not in s:
        raise PPDSParseError(f"positional args error: {s} is not a proper positional argument")

    return s.strip()

def extract_valid_kw_arg(s):


    byeq = s.split("=")
    name = byeq[0]
    val = "=".join(byeq[1:])

    return name.strip(), val.strip()


_flip = {"(":")", "[":"]", "{":"}"}
def split_smart(s):

    bracket_stack = []
    result_list = []
    current_str = []

    def finalize_arg():
        nonlocal current_str,result_list
        result_list.append("".join(current_str).strip())
        current_str = []

    for i,c in enumerate(s):
        if c == "," and len(bracket_stack)==0:
            finalize_arg()
            continue
        current_str.append(c)
        if c in "([{":
            bracket_stack.append(c)
        elif c in ")]}":
            if len(bracket_stack) > 0:
                t = bracket_stack.pop()
                if _flip[t] != c:
                    raise PPDSParseError(s+" has invalid brackets", position=i)
            else:
                raise PPDSParseError(s+ " closes bracket before ")
    finalize_arg()

    return result_list
