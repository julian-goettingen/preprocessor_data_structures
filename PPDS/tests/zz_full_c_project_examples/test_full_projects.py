# necessary boilerplate for importing stuff from the root-dir of the project
import sys

import tests.test_helpers.utils_for_testing as tut
import pytest
import itertools as it

parametrize = pytest.mark.parametrize



@parametrize(
    ("compiler", "dir"), it.product(tut.compiler_list.items(), tut.test_dir_list)
)
def test_integration(dir, compiler):

    tut.auto_try_dir(dir, compiler)


#
# @parametrize("compiler", tut.compiler_list)
# def test_can_compile(compiler):
#
#     tut.should_pass("tests/should_pass", compiler)
#
#
# @parametrize("compiler", tut.compiler_list)
# def test_fail(compiler):
#
#     tut.should_fail(compiler)
