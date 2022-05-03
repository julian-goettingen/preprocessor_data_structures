# necessary boilerplate for importing stuff from the root-dir of the project
import sys
import os.path
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))


import utils_for_testing as tut
import pytest
parametrize = pytest.mark.parametrize

@parametrize("compiler", tut.compiler_list)
def test_standard(compiler):

    tut.try_dir(
    os.path.dirname(__file__),
    tut.DirResult.runtime_error,
    ["ASSERTION FAILURE", "OUT OF BOUNDS"]
    )
