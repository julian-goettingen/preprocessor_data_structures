import subprocess
import io
from enum import IntEnum
import json
import os.path
import sys
from glob import glob

from dataclasses import dataclass
from typing import List


compiler_list = [
"gcc -std=c11 -fdiagnostics-color=always",
"gcc -std=c99 -fdiagnostics-color=always",
"gcc -std=gnu11 -fdiagnostics-color=always",
"gcc -std=gnu99 -fdiagnostics-color=always",
"g++ -fdiagnostics-color=always",
# "tcc",
"clang"
]

def find_dirs():

    cdirs = list(map(lambda p: os.path.dirname(p), glob("tests/full_examples/**/main.c")))

    return cdirs

test_dir_list = find_dirs()


@dataclass
class Compiler():
    name : str
    flags: List[str]
    is_cpp: bool



def run_process(cmd, timeout=0.5):


    res = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout)

    return res

def expect_success(sp_res, stage):

    if sp_res.returncode == 0:
        assert sp_res.stderr == b""

        # ret code 0 and no stderr output --> success
        return

    # report failure
    print(f"failed in stage: '{stage}'.\n#####stdout of failed action:", file=sys.stderr)
    sys.stderr.buffer.write(sp_res.stdout) # -> this writes bytes to stdout directly, keeping special stuff like colors and symbols
    print("########### stderr of failed action:", file=sys.stderr)
    sys.stderr.buffer.write(sp_res.stderr) # -> this writes bytes to stdout directly, keeping special stuff like colors and symbols
    print("########### Output end", file=sys.stderr)
    raise AssertionError(f"PROCESS FAILED with ret={sp_res.returncode}")

def expect_failure(sp_res, *msgs):

    assert sp_res.returncode != 0

    err_ci = str(sp_res.stderr).upper()

    for m in msgs:
        m = m.upper()
        assert m in err_ci

class DirResult(IntEnum):

    ppds_error = 1
    compile_error = 2
    runtime_error = 3
    no_error = 4

def try_dir(dir, expected_result,*, msgs=[], compiler="gcc"):

    main_path = os.path.join(dir, "main.c")

    # ppds-step
    res = run_process(f"python3 src/main.py {main_path}")
    if expected_result == DirResult.ppds_error:
        expect_failure(res,*msgs)
        return
    expect_success(res, "PREPROCESS WITH PPDS")

    # compile-step
    res = run_process(f"{compiler} -Wall -Wextra -Werror {main_path} -Ippds_source_headers -Ippds_target_headers" )
    if expected_result == DirResult.compile_error:
        expect_failure(res,*msgs)
        return
    expect_success(res, "COMPILE C CODE")

    # run-step
    res = run_process("./a.out")
    if expected_result == DirResult.runtime_error:
        expect_failure(res,*msgs)
        return
    expect_success(res, "RUN COMPILED BINARY")

def auto_try_dir(dir, compiler="gcc"):

    xpfile = os.path.join(dir, "expect.json")

    if not os.path.exists(xpfile):
        try_dir(dir, DirResult.no_error, compiler=compiler)
        return # success

    with open(xpfile, "r") as f:
        xpect = json.load(f)

    if "err_contains" not in xpect.keys():
        xpect["err_contains"] = []

    try_dir(dir, DirResult[xpect["res"]], msgs=xpect["err_contains"], compiler=compiler)
    # get expected result and message from expect.json



def should_pass(dir, compiler):

    try_dir(dir, DirResult.no_error, compiler = compiler)

def should_fail(compiler):

    try_dir("tests/should_fail", DirResult.runtime_error, msgs=["ASSERTION FAILURE", "OUT OF BOUNDS"],compiler= compiler)
    #auto_try_dir("tests/should_fail", compiler=compiler)
