import subprocess
import io
from enum import IntEnum
import os.path


compiler_list = [
"gcc -std=c11",
#"tcc",
#"gcc -std=c89",
"clang"
]


def run_process(cmd):


    res = subprocess.run(cmd, shell=True, capture_output=True)

    return res

def expect_success(sp_res):

    if sp_res.returncode == 0:
        assert sp_res.stderr == b""

        # ret code 0 and no stderr output --> success
        return

    # failure
    raise AssertionError(f"PROCESS FAILED with ret={sp_res.returncode}, stderr-output is:\n{sp_res.stderr}")

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

def try_dir(dir, expected_result, msgs=[], compiler="gcc"):

    main_path = os.path.join(dir, "main.c")

    # ppds-step
    res = run_process(f"python3 gen_ds_new.py {main_path}")
    if expected_result == DirResult.ppds_error:
        expect_failure(res,*msgs)
        return
    expect_success(res)

    # compile-step
    res = run_process(f"{compiler} -DNDEBUG=1 -Wall -Wextra -Werror {main_path} -Ippds_source_headers -Ippds_target_headers" )
    if expected_result == DirResult.compile_error:
        expect_failure(res,*msgs)
        return
    expect_success(res)

    # run-step
    res = run_process("./a.out")
    if expected_result == DirResult.runtime_error:
        expect_failure(res,*msgs)
        return
    expect_success(res)


def should_pass(dir, compiler):

    try_dir(dir, DirResult.no_error, compiler)

def should_fail(compiler):

    try_dir("tests/should_fail", DirResult.runtime_error, ["ASSERTION FAILURE", "OUT OF BOUNDS"], compiler)
