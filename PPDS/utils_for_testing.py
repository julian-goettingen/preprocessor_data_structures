import subprocess


def should_pass():
    
    res = subprocess.run("python3 gen_ds_new.py tests/should_pass/array_example.c")
    assert res.return_code == 0

    res = subprocess.run("clang -DNDEBUG=1 -Wall tests/should_fail/array_example.c -Ippds_source_headers -Ippds_target_headers")
    assert res.return_code == 0

    res = subprocess.run("./a.out")
    assert res.return_code == 0
