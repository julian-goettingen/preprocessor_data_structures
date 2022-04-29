import subprocess
import io


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

    for m in msgs:
        m = m.encode("UTF-8")
        assert m in sp_res.stderr


def should_pass():

    res = run_process("python3 gen_ds_new.py tests/should_pass/array_example.c")
    expect_success(res)

    res = run_process("clang -DNDEBUG=1 -Wall tests/should_pass/array_example.c -Ippds_source_headers -Ippds_target_headers")
    expect_success(res)

    res = run_process("./a.out")
    expect_success(res)


def should_fail():

    res = run_process("python3 gen_ds_new.py tests/should_fail/array_example.c")
    expect_success(res)

    res = run_process("clang -DNDEBUG=1 -Wall tests/should_fail/array_example.c -Ippds_source_headers -Ippds_target_headers")
    expect_success(res)

    res = run_process("./a.out")
    expect_failure(res, "ASSERTION FAILURE")
