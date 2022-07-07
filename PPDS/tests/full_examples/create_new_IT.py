
import re
import json
import os
import sys


default_expect_success = '{"res": "no_error"}'
default_expect_runtime_failure = '{"res": "runtime_error", "err_contains": ["ASSERTION FAILURE"]}'
default_expect_compile_error = '{"res": "compile_error", "err_contains": []}'
default_expect_ppds_error = '{"res": "ppds_error", "err_contains": []}'
default_expect = "\n\n".join([default_expect_ppds_error, default_expect_success, default_expect_runtime_failure, default_expect_compile_error])
empty_c = r"""
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    assert(x!=NULL);
    for (int i=0; i<n; i++) {
        x[i] = i;
    }


    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"

"""

for dir in sys.argv[1:]:

    if os.path.exists(dir):
        print(dir, " exists, will not create it")
        continue

    os.mkdir(dir)

    try:
        os.chdir(dir)

        with open("main.c", "w") as f:
            f.write(empty_c)

        if re.search(r"pass|success|work", dir.lower()):

            with open("expect.json", "w") as f:
                f.write(default_expect_success)

            os.system("atom --new-window main.c &")
        else:
            with open("expect.json", "w") as f:
                f.write(default_expect)

            os.system("atom --new-window main.c expect.json &")


    finally:
        os.chdir("..")
