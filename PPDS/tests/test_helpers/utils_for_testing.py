import subprocess
import io
from enum import IntEnum
import json
import os.path
import sys
from glob import glob

from dataclasses import dataclass
from typing import List


compiler_list = {
    "gcc c11": {"call":"gcc -std=c11 -fdiagnostics-color=always", "abilities": {"c11", "c"}},
    "gcc c99": {"call": "gcc -std=c99 -fdiagnostics-color=always", "abilities": {"c99", "c"}},
    "gcc gnu11": {"call": "gcc -std=gnu11 -fdiagnostics-color=always", "abilities": {"c11", "c", "gnu"}},
    "gcc gnu99": {"call": "gcc -std=gnu99 -fdiagnostics-color=always", "abilities": {"c99", "c", "gnu"}},
    "g++": {"call": "g++ -fdiagnostics-color=always", "abilities": {"cpp", "gnu"}},
    # "tcc", # get this to work? need to install it from source though...
    "clang": {"call": "clang -fdiagnostics-color=always", "abilities": {"c"}},
    "clang++": {"call": "clang++ -x c++ -fdiagnostics-color=always", "abilities": {"cpp"}}, # this call is so weird because it needs to compile .c files as c++ without complaining
}

def find_dirs():

    pattern = "tests/zz_full_c_project_examples/**/main.c"
    cdirs = list(map(lambda p: os.path.dirname(p), glob(pattern)))

    if not cdirs:
        raise ValueError(f"found no projects for test-build. glob-pattern is {pattern}, working dir is {os.getcwd()}")

    return cdirs

test_dir_list = find_dirs()


@dataclass
class Compiler():
    name : str
    flags: List[str]
    is_cpp: bool



def run_process(cmd, timeout=5, cwd=None):

    res = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout, cwd=cwd)

    return res

def expect_success(sp_res, stage, stderr_non_empty_ok=False):

    if sp_res.returncode == 0 and sp_res.stderr == b"":

        print("stderr empty & succ")
        # ret code 0 and no stderr output --> success
        return

    if sp_res.returncode == 0 and stderr_non_empty_ok:

        print("stderr non-empty & succ")
        # tolerate the stderr-output
        return

    errlen = len(sp_res.stderr)

    # report failure
    print(f"failed in stage: '{stage}'.\n#####stdout of failed action:", file=sys.stderr)
    sys.stderr.buffer.write(sp_res.stdout) # -> this writes bytes to stdout directly, keeping special stuff like colors and symbols
    print("\n########### stderr of failed action:", file=sys.stderr)
    sys.stderr.buffer.write(sp_res.stderr) # -> this writes bytes to stdout directly, keeping special stuff like colors and symbols
    print("########### Output end", file=sys.stderr)
    raise AssertionError(f"PROCESS FAILED with ret={sp_res.returncode} and {errlen} characters in stderr")

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

def try_dir(dir, expected_result,*, require=set(), stderr_non_empty_ok=False, msgs=[], compiler=None):

    main_path = os.path.join(dir, "main.c")

    if compiler is None:
        raise ValueError("need a compiler")

    # compilers should really be objects not this hot mess of dicts
    comp_name, comp_call, comp_abilities = compiler[0], compiler[1]["call"], set(compiler[1]["abilities"])

    if (not require.issubset(comp_abilities)):
        # skip bc compiler cant compile this
        # this is a success which is kinda wrong but skips would be confusing
        return
    

    def cleanup():
        res = run_process(f"make clean", cwd=dir)
        if (res.returncode != 0): # make clean really should not fail
            raise AssertionError(f"make clean failed with {res.returncode}, {res.stderr}")
    
    # cleanup before each test to give it a fresh start, but cleanup afterwards also. Overkill? maybe
    cleanup()
    try:
        # ppds-step
        res = run_process(f"make prepare", cwd=dir)
        if expected_result == DirResult.ppds_error:
            expect_failure(res,*msgs)
            return
        expect_success(res, "PREPROCESS WITH PPDS", stderr_non_empty_ok)

        # compile-step
        res = run_process(f'CC="{comp_call} -Wall -Wextra -Werror" make compile ', cwd=dir)
        if expected_result == DirResult.compile_error:
            expect_failure(res,*msgs)
            return
        expect_success(res, f"COMPILE C CODE with compiler {comp_name}", stderr_non_empty_ok)

        # run-step
        res = run_process("./a.out", cwd=dir)
        if expected_result == DirResult.runtime_error:
            expect_failure(res,*msgs)
            return
        expect_success(res, f"RUN COMPILED BINARY of {comp_name}", stderr_non_empty_ok)
    finally:
        cleanup()

def auto_try_dir(dir, compiler=None):

    xpfile = os.path.join(dir, "expect.json")

    if not os.path.exists(xpfile):
        raise ValueError("test folder must have an 'expect.json' file detailing what is expected from the test")

    with open(xpfile, "r") as f:
        xpect = json.load(f)

    # there are cleaner way to set defaults, replace this with dict.update() when it gets any bigger
    if "err_contains" not in xpect.keys():
        xpect["err_contains"] = []
    
    if "stderr_non_empty_ok" not in xpect.keys():
        xpect["stderr_non_empty_ok"] = False
    
    if "require" not in xpect.keys():
        xpect["require"] = []
    xpect["require"] = set(xpect["require"])

    try_dir(dir, DirResult[xpect["res"]], require=xpect["require"], stderr_non_empty_ok=xpect["stderr_non_empty_ok"], msgs=xpect["err_contains"], compiler=compiler)
    # get expected result and message from expect.json



def should_pass(dir, compiler):

    try_dir(dir, DirResult.no_error, compiler = compiler)

def should_fail(compiler):

    try_dir("tests/should_fail", DirResult.runtime_error, msgs=["ASSERTION FAILURE", "OUT OF BOUNDS"],compiler= compiler)
    #auto_try_dir("tests/should_fail", compiler=compiler)
