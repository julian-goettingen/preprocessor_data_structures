from ppds_pygen_usables.server_utils import CommandBuilder, CommandExecutor, PythonSimpleDataServer, build_arr_meta, obj_from
import io
import math
import numpy as np
import pytest
import itertools as it
import numpy.testing as npt
parametrize = pytest.mark.parametrize


def test_arr_meta1D():

    arr_meta = build_arr_meta([b"1D", 5, b"C", b"<f4"])
    assert(arr_meta.get_size() == 20)

def test_arr_meta3D():

    arr_meta = build_arr_meta([b"3D", 5, 3, 2, b"C", b"<f8"])
    assert(arr_meta.get_size() == 240)


@parametrize("arg", [1,0.5, -3,1e5,-2.7])
def test_obj_from(arg):

    argTransf = obj_from(bytes(str(arg), encoding="utf-8") )

    assert(arg == argTransf)

def test_obj_from_bytes():

    assert(b'hello' == obj_from(b'hello'))

def test_obj_from_nan():

    assert(math.isnan(obj_from("NaN")))



def test_can_finish():

    cb = CommandBuilder()
    cb.append(b"FINISH;")
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"FINISH"]])

def test_ignore_trailing():

    cb = CommandBuilder()
    cb.append(b"FINISH;FIN")
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"FINISH"]])

def test_continue_on_trailing():

    cb = CommandBuilder()
    cb.append(b"FINISH;FIN")
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"FINISH"]])
    cb.append(b"ISH;")
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"FINISH"]])

def test_no_args_call():

    cb = CommandBuilder()
    cb.append(b"START_CALL;foo;END_CALL;")
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"START_CALL", b"foo", b"END_CALL"]])

def test_no_args_call_split():

    cmds = []

    cb = CommandBuilder()
    cb.append(b"START_CALL;fo")
    cb.append(b"o;END_CALL;")
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"START_CALL", b"foo", b"END_CALL"]])

@parametrize("s", list(range(15)))
def test_no_args_call_split_arbitrary(s):

    cmds = []

    cb = CommandBuilder()
    raw = b"START_CALL;foo;END_CALL;"
    cb.append(raw[:s])
    cmds = cb.pop_finished_cmds()
    cb.append(raw[s:])
    cmds.extend(cb.pop_finished_cmds())
    assert(cmds == [[b"START_CALL", b"foo", b"END_CALL"]])


def test_number_args():

    cb = CommandBuilder()
    raw = b"START_CALL;foo;1;3;5.0;END_CALL;"
    cb.append(raw)
    cmds = cb.pop_finished_cmds()
    assert(cmds == [[b"START_CALL", b"foo", 1, 3, 5.0, b"END_CALL"]])


@parametrize(("a", "b"), it.product([0,3,7,11],[0,1,10]))
def test_mixed_call_split_arbitrary(a,b):

    cb = CommandBuilder()
    raw = b"START_CALL;foo;1;3;5.0;END_CALL;START_CALL;bar;END_CALL;FINISH;"
    cb.append(raw[:a])
    cb.append(raw[a:a+b])
    cb.append(raw[a+b:])
    cmds = cb.pop_finished_cmds()
    assert(cmds == [ 
        [b"START_CALL", b"foo", 1, 3, 5.0, b"END_CALL"], 
        [b"START_CALL", b"bar",b"END_CALL"],
        [b"FINISH"],
        ])

def test_dont_return_cmd_until_finished():

    cb = CommandBuilder()
    cb.append(b"START_CALL;foo;1;END_CA")
    cmds = cb.pop_finished_cmds()
    assert([] == cmds)
    cb.append(b"LL;")
    cmds = cb.pop_finished_cmds() 
    assert(cmds == [[b"START_CALL", b"foo", 1, b"END_CALL"]])


dtype_list = [b"<f4", b"<u2", b"=i4", b">f8", b"<f8"]

@parametrize("dt", dtype_list )
def test_trivial_array(dt):

    cb= CommandBuilder()
    raw_arr = np.array([1],dtype=dt).tobytes()

    cb.append(b"START_CALL;arr_func;[1D,1,C,"+dt+b",:"+raw_arr+b"];END_CALL;")

    cmds = cb.pop_finished_cmds()

    assert(np.all(cmds[0][2] == np.array([1],dtype=dt)))
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])


@parametrize("dt", dtype_list)
def test_longer_1d_array(dt):

    cb = CommandBuilder()
    ls = [1,2,3,4,5]
    raw_arr = np.array(ls,dtype=dt).tobytes()

    cb.append(b"START_CALL;arr_func;[1D,5,C,"+dt+b",:"+raw_arr+b"];END_CALL;")

    cmds = cb.pop_finished_cmds()
    assert(np.all(cmds[0][2] == np.array(ls,dtype=dt)))
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])



@parametrize(("dt","ordering"), it.product(dtype_list,[b"F", b"C"]))
def test_2d_array(dt, ordering):


    cb = CommandBuilder()
    ls = [[1,2],[3,4]]
    raw_arr = np.array(ls,dtype=dt).tobytes(order=ordering)

    cb.append(b"START_CALL;arr_func;[2D,2,2,"+ordering+b","+dt+b",:"+raw_arr+b"];END_CALL;")

    cmds = cb.pop_finished_cmds()
    npt.assert_array_equal(cmds[0][2],np.array(ls, dtype=dt, order=ordering))
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])


@parametrize("dt", dtype_list)
def test_non_square_2d_array_C(dt):

    cb = CommandBuilder()
    ls = [[1,2,3],[4,5,6]]
    raw_arr = np.array(ls,dtype=dt).tobytes()

    cb.append(b"START_CALL;arr_func;[2D,2,3,C,"+dt+b",:"+raw_arr+b"];END_CALL;")

    cmds = cb.pop_finished_cmds()
    npt.assert_array_equal(cmds[0][2],np.array(ls, dtype=dt))
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])

@parametrize("dt", dtype_list)
def test_non_square_2d_array_F(dt):

    cb = CommandBuilder()
    ls = [[1,2,3],[4,5,6]]
    raw_arr = np.array(ls,dtype=dt).tobytes(order="F")

    cb.append(b"START_CALL;arr_func;[2D,2,3,F,"+dt+b",:"+raw_arr+b"];END_CALL;")

    cmds = cb.pop_finished_cmds()
    npt.assert_array_equal(cmds[0][2],np.array(ls, dtype=dt))
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])


@parametrize("dt", dtype_list)
def test_5d_array(dt):

    cb = CommandBuilder()
    ls = list(range(5*6*7*8*9))
    arr = np.reshape(np.array(ls,dtype=dt),(5,6,7,8,9),order="F")
    raw_arr = arr.tobytes(order="F")

    cb.append(b"START_CALL;arr_func;[5D,5,6,7,8,9,F,"+dt+b",:"+raw_arr+b"];END_CALL;")

    cmds = cb.pop_finished_cmds()
    npt.assert_array_equal(cmds[0][2], arr)
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])

@parametrize(("a", "b"), it.product([10,13,20,26],[27,301,713]))
def test_array_arg_split_arbitrary(a,b):
    dt = b"<f4"
    cb = CommandBuilder()
    ls = list(range(5*6*7*8*9))
    arr = np.reshape(np.array(ls,dtype=dt),(5,6,7,8,9),order="F")
    raw_arr = arr.tobytes(order="F")

    raw = b"START_CALL;arr_func;[5D,5,6,7,8,9,F,"+dt+b",:"+raw_arr+b"];END_CALL;"
    cb.append(raw[:a])
    cb.append(raw[a:a+b])
    cb.append(raw[a+b:])

    cmds = cb.pop_finished_cmds()
    npt.assert_array_equal(cmds[0][2], arr)
    cmds[0][2] = None
    assert(cmds == [[b"START_CALL", b"arr_func", None, b"END_CALL"]])

class CommandExecutorTestable(CommandExecutor):

    def __init__(self):
        super().__init__()
        self.funcs_called = []

    def f1(self, a):
        self.funcs_called.append("f1")
        assert(a == 3)


    def f2(self, a,b):
        self.funcs_called.append("f2")
        assert(a == 3)
        assert(b == 4)

class DataServerTestable(PythonSimpleDataServer):

    def __init__(self, bytesio):
        self.funcs_called = []
        super().__init__(bytesio)

    def f1(self, a):
        print("calling f1")
        self.funcs_called.append("f1")
        assert(a == 3)
        print("funcs called set to: ", self.funcs_called)

    def f2(self, a,b):
        self.funcs_called.append("f2")
        assert(a == 3)
        assert(b == 4)
    
    def die(self, exit_code):
        assert(exit_code == 0)
        raise InterruptedError("has finished successfully")


def test_command_executor_simple():

    ce = CommandExecutorTestable()
    ce.exec_cmd([b"START_CALL", b"f1", 3, b"END_CALL"])
    assert(ce.funcs_called == ["f1"])

def test_command_executor_multiple_funcs():

    ce = CommandExecutorTestable()
    ce.exec_cmd([b"START_CALL", b"f1", 3, b"END_CALL"])
    ce.exec_cmd([b"START_CALL", b"f2", 3, 4, b"END_CALL"])
    ce.exec_cmd([b"START_CALL", b"f1", 3, b"END_CALL"])
    assert(ce.funcs_called == ["f1", "f2", "f1"])


def test_PythonSimpleDataServer():
    b = io.BytesIO(b"START_CALL;f1;3;END_CALL;FINISH;")
    srv = DataServerTestable(b)

    with pytest.raises(InterruptedError):
        srv.run()

    assert(srv.funcs_called == ["f1"])
    