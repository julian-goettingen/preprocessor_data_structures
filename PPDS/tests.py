import utils_for_testing as tut
import pytest

parametrize = pytest.mark.parametrize

compiler_list = [
"gcc -std=c11",
#"tcc",
#"gcc -std=c89",
"clang"
]

#compiler_list = ["gcc"]

@parametrize("compiler", compiler_list)
def test_can_compile(compiler):

    tut.should_pass("tests/should_pass", compiler)


@parametrize("compiler", compiler_list)
def test_fail(compiler):

    tut.should_fail(compiler)
