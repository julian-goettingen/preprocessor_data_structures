import os
from abc import ABC
from typing import Dict, Any, Tuple, TextIO
import re


from src.sinks import HeaderStack, PPDSTargetFile

from src.PreprocessorDataClass import (
    PreprocessorDataClass,
    PreprocessorDataClassInstance,
)
from src.config import get_config
from src.parse import scan_arglist_till_closing_bracket
from src.parse_err import PPDSParseError

# das main-loop muss geändert werden, damit $A durch das dictionary von A ersetzt werden können.
# Vielleicht kann man dabei auch den target-file-stack durch ein intelligenteres producer-consumer-konzept ersetzt werden.
# Jede Zeile kann eines von diesen sein:
# ein def-file öffnen (mit #include PPDS_DEF...)
DEF_REX_STR = r'#include\s+"(?P<target_def_filename>PPDS_DEF_\w+\.h)"'
# ein def-file schließen (mit #include PPDS_TARGET_UNDEF...)
UNDEF_REX_STR = r'#include\s+"(?P<target_undef_filename>PPDS_UNDEF_\w+\.h)"'
# eine Klasse hinzufügen (mit #include PPDS_SOURCE...)
SOURCE_REX_STR = (
    r'#include\s+"(?P<source_filename>PPDS_SOURCE_(?P<datastructure_name>\w+)\.h)"'
)
# eine Klasse instanziieren (mit PPDS_DECLARE_)
DECLARE_REX_STR = r"PPDS_DECLARE_(?P<declare_type>\w+)\s*\("

PPDS_ACTION_REX = re.compile(r"|".join([DEF_REX_STR, UNDEF_REX_STR, SOURCE_REX_STR, DECLARE_REX_STR]))


def raise_unknown_dataclass(declare_type, classes):
    msg = []
    msg.append(f"Cannot declare PPDS-instance of unknown type {declare_type}")
    if len(classes) == 0:
        msg.append(
            f'There are no known types, add them with #include "PPDS_SOURCE_<name>.h"'
        )
    else:
        msg.append(f"Known dataclasses are: {classes.keys()}")
    raise PPDSParseError("\n".join(msg))

class PPDSKnownClasses:

    # ist das wirklich nötig?

    def __init__(self):
        self._classes : Dict[str, Tuple[PreprocessorDataClass, bool]] = {}
    
    def load_from_dir(self, source_header_loc):
        ...

    def activate(self, name):
        ...
    
    def deactivate_all(self):
        ...


def handle_file(src, defs_for_header_file: PPDSTargetFile, py_wrapper_file: PPDSTargetFile, _get_config=get_config):

    conf = _get_config()

    # keys are names
    classes: Dict[str, PreprocessorDataClass] = {}

    # keys are names, values are PreprocessorDataClassInstances transformed to dicts
    instances: Dict[str, PreprocessorDataClassInstance] = {}

    # header-stack
    headers = HeaderStack(target_header_loc=conf.target_header_loc)

    # todo: string-slices are copies, not views, so this is very inefficient.
    # is that the main reason this is slow?

    while src:
        m = PPDS_ACTION_REX.search(src)
        if not m:
            break  # finished
        src = src[m.end() :]
        declare_type = m.group('declare_type')
        if declare_type:
            # a new instance of a dataclass, scan the arguments and create it (to put it in the classes)
            klass = classes.get(declare_type)
            if klass is None:
                raise_unknown_dataclass(declare_type, classes)
            arglist, src = scan_arglist_till_closing_bracket(src) # part of src is consumed here
            inst = klass.make_instance(
                arglist, declare_site="(TODO)", known_objects=instances
            )  # todo: declare_site
            instances[inst.name.get_value()] = inst


            print('added instance: ', inst)
            headers.new_instance(inst)
            defs_for_header_file.append(inst.render_defs_for_header())
            py_wrapper_file.append(inst.render_py_wrapper())

            continue
        target_def_filename = m.group("target_def_filename")
        if target_def_filename:
            # how to handle undef with functions?
            # a new def-header, use in stack
            headers.new_def(target_def_filename)
            continue
        target_undef_filename = m.group('target_undef_filename')
        if target_undef_filename:
            # a new undef-header, close file in stack if correct else throw
            headers.new_undef(target_undef_filename)
            continue
        source_filename = m.group("source_filename")
        if source_filename:
            # a new dataclass, read it and put it in the list of classes

            ds_name = m.group("datastructure_name")
            assert ds_name is not None

            with open(os.path.join(conf.source_header_loc, source_filename)) as f:
                source_string = f.read()
            classes[ds_name] = PreprocessorDataClass(ds_name, source_string)
            print("new class added: ", ds_name)

    if len(headers) > 0:
        raise PPDSParseError(f"target-defs left open: {headers}")


# notes on error-handling
# double-declaring a source could easily be caught
# the line-numbers can be retrieved with this rfind-method: https://stackoverflow.com/questions/16673778/python-regex-match-in-multiline-but-still-want-to-get-the-line-number
# besser geht es noch wenn man einfach auf die Länge guckt während man den string frisst und dazwischen die newlines zählt.

# Es können auch schon standard-consumer existieren (für python und .c boilerplate?)

# notes on perf
# sources could easily be cached

# mockability:
# das file-öffnen könnte man komplett aus der Methode lassen oder? Da würde man die gleiche Struktur wie beim cachen einziehen


# logging sollte standardisiert werden.
