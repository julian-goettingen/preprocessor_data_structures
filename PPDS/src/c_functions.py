from pycparser import c_parser
from dataclasses import dataclass
import re
from typing import List, Union, Match


@dataclass
class CFunctionArrayParam:
    name: str
    primitive_type: str
    pointer_type: str
    dims: List[int]

def make_c_function_array_param(decl):
    print("making class of: ", decl)
    return None


@dataclass
class CFunctionPrimitiveParam:
    name: str
    primitive_type: str


@dataclass
class CFunctionDef:
    name: str
    rettype: str
    params: List[Union[CFunctionArrayParam, CFunctionPrimitiveParam]]


# consts
parser = c_parser.CParser()
arrdeclare_rex = re.compile(r"ARR\dD_ARG\([^)]+\)")
SPECIAL_PPDS_PSEUDO_TYPE = "special_ppds_pseudo_type"



def _find_and_replace_arr_defs(text: str) -> (str, List[Match[str]]):

    matches = []

    def repl_and_collect(s: Match[str]):
        matches.append(s)
        return f"special_ppds_pseudo_type ppds_param_{len(matches)}"

    res = arrdeclare_rex.sub(repl_and_collect, text)
    return res, matches


def read_func_decl(text):

    # find array-definitions
    # parse array-definitions seperately
    # replace array-definitions with placeholders
    # parse remaining declaration with placeholders
    # replace placeholders with their real array-type


    text, matches = _find_and_replace_arr_defs(text)
    text = f"typedef int {SPECIAL_PPDS_PSEUDO_TYPE}; {text};"
    midx = 0

    ast = parser.parse(text)
    name = ast.ext[1].name
    rettype = ast.ext[1].type.type.type.names[0]
    params = []
    args = ast.ext[1].type.args
    if args: # empty args need special handling because otherwise args.params cant be accessed
        for p in args.params:
            typename = p.type.type.names[0]
            if typename == SPECIAL_PPDS_PSEUDO_TYPE:
                interpreted_param = make_c_function_array_param(matches[midx])
                midx+=1
            else:
                interpreted_param = CFunctionPrimitiveParam(p.name, p.type.type.names[0])
            params.append(interpreted_param)

    assert(midx == len(matches))

    return CFunctionDef(name, rettype, params)
