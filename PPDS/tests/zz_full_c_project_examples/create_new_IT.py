#!/bin/bash/python

import re
import json
import os
import sys


default_expect_success = '{"res": "no_error"}'
default_expect_runtime_failure = '{"res": "runtime_error", "err_contains": ["ASSERTION FAILURE"]}'
default_expect_compile_error = '{"res": "compile_error", "err_contains": []}'
default_expect_ppds_error = '{"res": "ppds_error", "err_contains": []}'
default_expect = "\n\n".join([default_expect_ppds_error, default_expect_success, default_expect_runtime_failure, default_expect_compile_error])
default_makefile = r"""

all:
	make prepare
	make compile

clean:
	rm -f ppds_interface_desc/*
	rm -f ppds_target_headers/*
	rm -f ./a.out

prepare:
	python3 ./../../../src/main.py

compile:
	${CC} main.c -Ippds_target_headers -I../../../ppds_source_headers

run:
	./a.out

"""
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

default_config = r"""
{
    "source_header_loc": "../../../ppds_source_headers",
    "target_header_loc": "./ppds_target_headers",
    "interface_desc_loc": "./ppds_interface_desc",
    "search_paths": ["./main.c"],
    "global_default_params": {}
}
"""


if( not (len(sys.argv) > 1)):
    print("needs argument")
    sys.exit(1)

for dir in sys.argv[1:]:

    if os.path.exists(dir):
        print(dir, " exists, will not create it")
        continue

    os.mkdir(dir)

    try:
        os.chdir(dir)

        with open("main.c", "w") as f:
            f.write(empty_c)

        with open("expect.json", "w") as f:
            f.write(default_expect)
        
        with open("Makefile", "w") as f:
            f.write(default_makefile)
        
        with open("ppds_config.json", "w") as f:
            f.write(default_config)
        
        os.mkdir("ppds_interface_desc")
        os.mkdir("ppds_target_headers")

        os.system("atom --new-window main.c expect.json &")



    finally:
        os.chdir("..")
