import pytest
import tests.test_helpers.utils_for_testing as tut
import itertools as it


dirs = []

# setup
def setup_module():

    dirs = tut.find_dirs()


@pytest.mark.parametrize("compiler, dir", it.product(tut.compiler_list, dirs))
def test_compile(compiler, dir):

    tut.auto_try_dir(compiler, dir)
