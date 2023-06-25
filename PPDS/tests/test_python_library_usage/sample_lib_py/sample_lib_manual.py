import pygen_usables
import numpy as np
import ctypes

_lib = ctypes.CDLL('../sample_lib/lib.so')

def hello_int(num):
    return _lib.hello_int_def(num)

def arr_sum(arr : np.ndarray):
    arr_ptr = np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags="C_CONTIGUOUS")
    print(arr_ptr)
    _lib.arr_sum_def.argtypes = [arr_ptr, ctypes.c_int]
    return _lib.arr_sum_def(arr, arr.shape[0])



if __name__ == "__main__":
    hello_int(3)
    print(arr_sum(np.array([1,2,3], dtype=np.float64)))

#
# sollte das eine Klasse sein? erstmal nicht, einfach funktionen, ist erstmal leichter.
# Die Funktionen können ja aus der function-def rausfallen.
