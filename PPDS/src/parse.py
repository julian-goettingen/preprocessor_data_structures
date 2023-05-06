import copy
import re
from parse_err import PPDSParseError
from typing import Dict, Any, Tuple, List, Union


def make_arg_dict(posargs, default_kwargs, argstring):

    user_args = parse_args_string(argstring, posargs, default_kwargs)

    # initialize with defaults from the header-file and the global config
    argdict = {**default_kwargs}

    # the actual parameters passed in have the highest precedence
    argdict.update(user_args)

    return argdict

# this module is a mess but I only use parts of the code and there are lot of tests, TODO: refactor after big change of main
# TODO: die specials sind noch broken in der neuen main (?)

def is_positional(arg: str) -> bool:

    if "=" in arg and "==" not in arg: # todo: this criterium is pretty much bs
        return False
    return True

def raw_arglist_to_initialized_argdict(arglist: List[str], posarglist: List[str], kwargs: Dict[str, str]) -> Dict[str, Union[str, List[str]]]:



    # check if number of positional arguments is OK
    # empty for positional arguments is allowed
    if len(arglist) < len(posarglist) - 1 or posarglist[-1] != "_var_args_" and len(arglist) < len(posarglist):
        raise PPDSParseError(
            "Not enough positional arguments",
            detail=f"arglist {arglist} of length {len(arglist)} cannot satisfy required positional arguments {posarglist}")

    argdict : Dict[str, Union[str, List[str]]] = copy.deepcopy(kwargs)

    if posarglist[-1] == "_var_args_":
        argdict["var_args"] = []

    # loops over arglist; is a statemachine on state 'mode'
    mode = 0 # 0-> normal pos-arg, 1-> vararg, 2-> keyword-arg
    for i, arg in enumerate(arglist):

        if i < len(posarglist) and posarglist[i] == "_var_args_" and not i == len(posarglist)-1:
            raise ValueError(f"illegal template has _var_args_ at position {i}")

        #################
        # STATE TRANSITIONS::
        if mode == 0 and i == len(posarglist):
            mode = 2
        if mode == 0 and i == len(posarglist) - 1 and posarglist[i] == "_var_args_":
            mode = 1  # potentially triggering the next condition
        if mode == 1 and not is_positional(arg):
            mode = 2


        #####################
        # READING ARGUMENT::
        if mode == 0:
            val = extract_valid_pos_arg(arg)
            argdict[posarglist[i]] = val
        elif mode == 1:
            val = extract_valid_pos_arg(arg)
            argdict["var_args"].append(val)
        elif mode == 2:
            name, val = extract_valid_kw_arg(arg)
            argdict[name] = val
        else:
            raise ValueError(f'mode must be 0, 1 or 2, was {mode}, this is a bug.')

    return argdict

def raw_arglist_to_argdict(arglist, posarglist, kwargnames):


    if len(arglist) < len(posarglist):
        raise PPDSParseError(
            "Not enough positional arguments",
            detail=f"arglist {arglist} of length {len(arglist)} cannot satisfy required {len(posarglist)} positional arguments {posarglist}",
        )

    argdict = {}

    argnum = 0
    # do positional arguments first
    for arg, argname in zip(arglist, posarglist):

        val = extract_valid_pos_arg(arg)
        argdict[argname] = val
        argnum += 1  # deliberately at bottom

    # iterate through the rest of arglist to get the keyword-args
    for arg in arglist[argnum:]:
        argname, val = extract_valid_kw_arg(arg)
        if argname not in kwargnames:
            raise PPDSParseError(
                f"{argname} is not a valid keyword-argument. Must be one of {kwargnames}"
            )
        argdict[argname] = val

    argdict = flatten_specials(argdict)

    return argdict


def parse_args_string(raw_args, posarglist, kwargnames):

    arglist = preprocess_raw_args(raw_args)

    return raw_arglist_to_argdict(arglist, posarglist, kwargnames)


COLON_REX = re.compile(r"(?<!:):(?!:)")  # matches ":" but not "::" to allow namespaces


def flatten_specials(argdict: Dict[str, str]):

    res = {}
    for k, v in argdict.items():
        m = COLON_REX.split(v)
        if len(m) == 1:
            # no special annotations; keep it as is
            res[k] = v
        elif len(m) == 2:
            # special annotations present; append them separately
            res[k] = m[0].strip()
            annotations = split_smart(m[1])
            for a in annotations:
                anno_dict = annotation_to_dict(a)
                flat_append_in_place(res, k, anno_dict)
        else:
            raise PPDSParseError(
                f"Illegal pattern of colons (':') in argument {v} for parameter {k},"
                f"an argument should be of the form"
                f'"val" or "val : extra_info(stuff)" or "val : extra_info(stuff), more_info(more_stuff)")'
                f"the c++-namespace-syntax ('::') is supported"
            )

    return res


TYPE_REX = re.compile(r"type\(([a-zA-Z0-9 *]+)\)")
ELEMENTTYPE_REX = re.compile(r"elementtype\((\w+)\)")
ISSAFE_REX = re.compile(r"issafe\((true|false)\)")
SPECIAL_REX = re.compile(r"special")


def annotation_to_dict(a: str):

    if m := TYPE_REX.match(a):
        return {"type": m.group(1)}
    elif m := ELEMENTTYPE_REX.match(a):
        return {"elementtype": m.group(1)}
    elif m := ISSAFE_REX.match(a):
        boolval = True if m.group(1) == "true" else False
        return {"issafe": boolval}
    elif m := SPECIAL_REX.match(a):
        return {"special": True}

    raise PPDSParseError(f"Unknown or misused annotation {a}")


def flat_append_in_place(
    dict1: Dict[str, Any], name_prefix: str, dict2: Dict[str, Any]
):

    for k, v in dict2.items():
        newkey = name_prefix + "_" + k
        if newkey in dict1:
            raise PPDSParseError(
                f"key {newkey} exists on \n{dict1}\n"
                f"therefore the extra information contained in \n{dict2}\n"
                f"cannot be added to it.\n"
                f"This is most likely due to a name conflict in the source-file for this datastructure."
            )
        dict1[newkey] = v


def preprocess_raw_args(raw_args):

    # only what is between the outermost brackets is an argument
    # remove everything except the stuff between them

    # todo: all of this should be handled by grammars not regexp
    m = re.match(r"\((.*)\)", raw_args)
    if not m:
        raise PPDSParseError("failed to parse arguments")

    args = split_smart(m.groups()[0])
    return args


# TODO: handle ==comparison and possibly even =assignment in brackets
# both this function and the one for keywords dont allow == sign in values
def extract_valid_pos_arg(s: str) -> str:

    if not is_positional(s):
        raise PPDSParseError(
            f"""
            positional args error: {s} is not a proper positional argument.
            It appears to be a keyword-argument but a positional argument was expected.
            """
        )

    return s.strip()


def extract_valid_kw_arg(s: str) -> Tuple[str, str]:

    if is_positional(s):
        raise PPDSParseError(
            f"Expected keyword argument but received what looks like a positional argument: {s}"
        )

    byeq = s.split("=")
    name = byeq[0]
    val = "=".join(byeq[1:])

    return name.strip(), val.strip()


_flip = {"(": ")", "[": "]", "{": "}"}


def split_smart(s):

    bracket_stack = []
    result_list = []
    current_str = []

    def finalize_arg():
        nonlocal current_str, result_list
        result_list.append("".join(current_str).strip())
        current_str = []

    for i, c in enumerate(s):
        if c == "," and len(bracket_stack) == 0:
            finalize_arg()
            continue
        current_str.append(c)
        if c in "([{":
            bracket_stack.append(c)
        elif c in ")]}":
            if len(bracket_stack) > 0:
                t = bracket_stack.pop()
                if _flip[t] != c:
                    raise PPDSParseError(s + " has invalid brackets", position=i)
            else:
                raise PPDSParseError(s + " closes bracket before end is reached")
    finalize_arg()

    return result_list


def scan_arglist_till_closing_bracket(s: str) -> Tuple[List[str], str]:

    bracket_stack = []
    result_list: List[str] = []
    current_str: List[str] = []

    def finalize_arg():
        nonlocal current_str, result_list
        result_list.append("".join(current_str).strip())
        current_str = []

    for i, c in enumerate(s):
        if c == "," and len(bracket_stack) == 0:
            finalize_arg()
            continue
        if c == ")" and len(bracket_stack) == 0:
            # NORMAL TERMINATION IS HERE ====>
            finalize_arg()
            print(f'scanning arglist gives: {result_list}')
            return result_list, s[i+1:]
            # <===============
        current_str.append(c)
        if c in "([{":
            bracket_stack.append(c)
        elif c in ")]}":
            if len(bracket_stack) > 0:
                t = bracket_stack.pop()
                if _flip[t] != c:
                    raise PPDSParseError(
                        f"Invalid brackets found, cannot terminate {t} with {c}\n{s[:i+10]}",
                        position=i,
                    )
            else:
                raise PPDSParseError(
                    f"closes bracket {c} before opening it", position=i
                )

    raise PPDSParseError(
        f"Unexpected end of input. Did you forget to close parentheses () around the arguments?"
    )
