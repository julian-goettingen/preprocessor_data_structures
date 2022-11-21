from dataclasses import dataclass
from enum import Enum
import numpy as np
import re
import sys
import os

CMD_END_REX = re.compile(rb"END_CALL|FINISH")


# builds a number or string from a bytearray
def obj_from(raw):

    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass

    return bytes(raw)


class ParseState(Enum):

    BUILD_ARR_DATA = 1
    BUILD_MAIN_ELEM = 2
    BUILD_ARR_META = 3
    EXPECT_SEMICOLON = 4
    EXPECT_CLOSING_BRACKET = 5


class CommandBuilder:
    def __init__(self):

        self.buff = bytearray()
        self.elems = []
        self.arr_meta_stack = []
        self.n_exp = "invalid"
        self.pst = ParseState.BUILD_MAIN_ELEM
        self.cmd_q = []

    # build this if debugging requires it
    # def _validate(self):

    #     if (self.pst == ParseState.BUILD_MAIN_ELEM):
    #         assert(self.arr_meta_stack == [])
    #         assert(self.n_exp == -1)
    #         assert(self.end_pattern )

    def pop_finished_cmds(self):

        ret = self.cmd_q
        self.cmd_q = []
        return ret

    # returns None
    def append(self, dat):

        print("buffer: ", self.buff, "  state: ", self.pst, "   dat: ", dat)
        print(self.cmd_q)

        # can happen through recursion. Also this makes sense for consistency
        if len(dat) == 0:
            return None

        if self.pst == ParseState.BUILD_ARR_DATA:
            # print("build_arr_data")

            # append the data to the buffer and decr the counter
            arr_dat = dat[: self.n_exp]
            self.buff.extend(arr_dat)
            self.n_exp -= len(arr_dat)
            if self.n_exp == 0:  # array is finished
                self.elems.append(self.arr_meta.make_arr(self.buff))
                self.buff = bytearray()
                self.arr_meta_stack = None
                end = len(arr_dat)
                self.n_exp = "invalid"
                self.pst = ParseState.EXPECT_CLOSING_BRACKET
                return self.append(dat[end:])
            elif self.n_exp < 0:
                raise ValueError(f"n_exp = {self.n_exp}, which is illegal")

        elif self.pst == ParseState.BUILD_MAIN_ELEM:

            # print('building main element with dat=',dat)
            # switch to array-meta-building if necessary
            if len(self.buff) == 0 and dat[0] == b'['[0]:
                # print('entering build_arr_meta')
                self.pst = ParseState.BUILD_ARR_META
                return self.append(dat[1:])
            # print('NOT entering build_arr_meta')

            # scan to character
            idx = dat.find(b';')
            if idx >= 0:  # current element finished
                # print("finishing element")
                self.buff.extend(dat[:idx])
                self.elems.append(obj_from(self.buff))
                # print(self.elems)
                self.buff = bytearray()

                last_elem = self.elems[-1]
                if isinstance(last_elem, bytes) and CMD_END_REX.match(self.elems[-1]):
                    self.cmd_q.append(self.elems)  # !sic, append as list
                    self.elems = []

                return self.append(dat[idx + 1 :])

            if idx == -1:
                self.buff.extend(dat)
                return None

        elif self.pst == ParseState.BUILD_ARR_META:

            # switch to array-data-building if necessary
            if len(self.buff) == 0 and dat[0] == b':'[0]:
                self.pst = ParseState.BUILD_ARR_DATA
                self.arr_meta = build_arr_meta(self.arr_meta_stack)
                self.arr_meta_stack = []
                self.n_exp = self.arr_meta.get_size()
                return self.append(dat[1:])

            # scan to character
            idx = dat.find(b',')
            self.buff.extend(dat[:idx])
            if idx >= 0:  # current element finished
                self.arr_meta_stack.append(obj_from(self.buff))
                self.buff = bytearray()
                return self.append(dat[idx + 1 :])

        elif self.pst == ParseState.EXPECT_SEMICOLON:

            if dat[0] != b";"[0]:
                raise ValueError(f"expected semicolon but got {dat[0]} instead")
            else:
                self.pst = ParseState.BUILD_MAIN_ELEM
                return self.append(dat[1:])

        elif self.pst == ParseState.EXPECT_CLOSING_BRACKET:

            if dat[0] != b"]"[0]:
                raise ValueError(
                    f"expected closing bracket ']' but got {dat[0]} instead"
                )
            else:
                self.pst = ParseState.EXPECT_SEMICOLON
                return self.append(dat[1:])

        else:
            raise ValueError("self.pst has unknown value " + self.pst)

        return None


# in the sections called rawbinarydata, everything is allowed, but the size is known
"""
START_CALL;function_name;arg1;arg2;[3D,nx,ny,nz,ordering,dtype_str,:n_bytes_of_rawbinarydata];arg4;END_CALL;
FINISH;
"""
# arrays are
# (no spaces)
# scannable without extra configuration!


@dataclass(frozen=True, eq=True)
class ArrMeta:
    dt: np.dtype
    dims: tuple[int]
    ordering: bytes

    def get_size(self):
        return self.dt.itemsize * np.prod(self.dims)

    def make_arr(self, buffer):

        assert len(buffer) == self.get_size()
        arr1D = np.frombuffer(buffer, dtype=self.dt)
        return np.reshape(arr1D, self.dims, self.ordering)


def build_arr_meta(arr_meta_stack):

    try:
        m = re.match(rb"([1-9][0-9]*)[Dd]", arr_meta_stack[0])
        ndims = int(m.group(1))
        dims = []
        for i in range(1, ndims + 1):
            dims.append(int(arr_meta_stack[i]))
        dims = tuple(dims)
        ordering = arr_meta_stack[i + 1]
        dt = np.dtype(arr_meta_stack[ndims + 2])

        if not re.match(rb"[CcFf]", ordering):
            raise ValueError(f"ordering must be C or F, was {ordering}")
    except Exception as e:
        raise ValueError(f"failed to handle argument stack: {arr_meta_stack}") from e

    return ArrMeta(dt, dims, ordering)


class CommandExecutor:
    def exec_cmd(self, cmd):
        if cmd[0] == b"START_CALL":
            assert cmd[-1] == b"END_CALL"
            func_name = cmd[1].decode("utf-8")
            args = cmd[2:-1]
            return self.__getattribute__(func_name)(*args)
        elif cmd[0] == b"FINISH":
            print("server exiting normally")
            self.die(0)
        else:
            raise ValueError("unknown command: ", cmd)



class PythonSimpleDataServer(CommandExecutor):
    def __init__(self, readsource=sys.stdin.buffer):
        self.cb = CommandBuilder()
        self.readsource = readsource

    def on_cmds(self, cmds):
        for c in cmds:
            print("calling exec_cmd with: ", c)
            self.exec_cmd(c)

    def on_not_found(self):
        os.sched_yield()
        # wait indefinitely, dont close

        # if not hasattr(self, "fin"):
        #     self.fin = 0
        # self.fin += 1
        # if self.fin == 10:
        #     print("server exiting due to not getting any data")
        #     self.die(1)

    def die(self, exit_code):
        print(f"server finishing with exit code {exit_code}")
        exit(exit_code)

    def run(self):

        while True:
            print("reading")
            r = self.readsource.read(100)
            print(getattr(self, "fin", "not initialized"), r)
            if r == b'':
                self.on_not_found()

            self.cb.append(r)
            cmds = self.cb.pop_finished_cmds()
            self.on_cmds(cmds)
