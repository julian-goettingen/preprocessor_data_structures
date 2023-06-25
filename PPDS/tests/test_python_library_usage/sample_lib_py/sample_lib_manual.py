import pygen_usables
import numpy as np
import ctypes

_lib = ctypes.CDLL('../sample_lib/lib.so')

def hello_int(num):
    return _lib.hello_int_def(num)

def arr_sum(arr : np.ndarray):
    assert len(arr.shape) == 1
    assert arr.dtype == np.float64
    # must assert the array is contiguous
    return _lib.arr_sum_def(arr.ctypes.data_as(ctypes.c_void_p), arr.shape[0])



if __name__ == "__main__":
    hello_int(3)
    print(arr_sum(np.array([1,2,3], dtype=np.float64)))

#
# sollte das eine Klasse sein? erstmal nicht, einfach funktionen, ist erstmal leichter.
# Die Funktionen können ja aus der function-def rausfallen.
