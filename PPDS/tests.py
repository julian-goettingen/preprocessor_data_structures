import utils_for_testing as tut
import pytest

parametrize = pytest.mark.parametrize


@parametrize("compiler", ["gcc", "clang"])
def test_can_compile(compiler):

    tut.should_pass(compiler)


@parametrize("compiler", ["gcc", "clang"])
def test_fail(compiler):

    tut.should_fail(compiler)
