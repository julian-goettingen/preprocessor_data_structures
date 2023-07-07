import re
import textwrap
import pathlib
import shutil
import os.path
from glob import glob

from src.handle_file import handle_file
from src.parse_err import PPDSParseError
from src.config import get_config
import src.util
from src.sinks import PPDSTargetFile

conf = get_config()


SOURCE_REX = r'\s+\#include\s+\"PPDS_SOURCE_(\w+?)\.h\"'


def_rex = re.compile(r'\#include\s+"PPDS_DEF_(\w+)\.h"')
undef_rex = re.compile(r'\#include\s+"PPDS_UNDEF_(\w+)\.h"')


def main():

    # conf-file over cmdline for most things
    ppds_source_header_dir = conf.source_header_loc
    ppds_target_header_dir = conf.target_header_loc
    # conf.pygen_target_loc
    # ppds_source_header_loc = conf.pygen_usables_loc


    if conf.pygen_target_loc is not None:
        pygen_target = pathlib.Path(conf.pygen_target_loc)
        usables_dest = os.path.join(pygen_target, "pygen_usables")
        os.makedirs(usables_dest, exist_ok=True)
        shutil.copytree(
            src=conf.pygen_usables_loc, dst=usables_dest, dirs_exist_ok=True
        )
        target_loc_init = os.path.join(pygen_target, "__init__.py")
        with open(target_loc_init, "w") as f:
            f.write("# \n")

    files = set()
    for s in conf.search_paths:
        if not isinstance(s, str):
            print("search paths must be strings, but in config file found: {s}")
            exit(1)
        matches = glob(s, recursive=True)
        print("matches: ", matches)
        files = files.union(set(glob(s)))
        if len(files) == 0:
            print("ERROR: no files found to prepare, glob-pattern was "+s)
            exit(1)

    print("ppds preparing files: ", files)

    py_loc = get_config().pygen_target_loc
    py_wrapper_filename = None if py_loc is None else os.path.join(py_loc, "py_wrapper.py")
    py_wrapper_file = PPDSTargetFile("py_wrapper", py_wrapper_filename)
    py_wrapper_file.append(textwrap.dedent(f"""
import pygen_usables
import numpy as np
import ctypes


_lib = ctypes.CDLL({get_config().compiled_lib_loc})

    """))

    for filename in files:
        with open(filename, 'r') as f:
            # preserves line numbers
            code = src.util.remove_comments(f.read())
        try:

            defs_for_header_filename = os.path.join(get_config().target_header_loc, filename.split('/')[-1].split('.')[0]+"_PPDS_GENERATED_DEFS_FOR_HEADER.h")
            defs_for_header = PPDSTargetFile(f"defs_for_{filename}", defs_for_header_filename)
            defs_for_header.append("\n// todo: include guards, notice etc\n")


            handle_file(code, defs_for_header, py_wrapper_file)


            defs_for_header.append("\n// todo: include guards, notice etc\n")
            defs_for_header.flush()

        except PPDSParseError as e:
            print(
                f"""
    ERROR related to file {filename} :

    {e.reason}

    {e.detail}
                """
            )
            exit(1)
        except Exception as e:
            print(f"""
        An unknown problem occured during parsing of your source-file. See stacktrace below.            
        This could be due to a error in your code or in PPDS.
        Even if your code is wrong, PPDS should be able to give you a hint on what is wrong with it, so please file a bug report.
        Problematic code is in file {filename}
        """)
            raise

    py_wrapper_file.flush()
