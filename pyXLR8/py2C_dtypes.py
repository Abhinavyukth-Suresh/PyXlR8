import numpy as np
import ctypes

class double:
    pass

class double_ptr:
    pointer = ctypes.POINTER(ctypes.c_double)
    def to_ptr(arr:np.array):
        return arr.ctypes.data_as(double_ptr.pointer)
    
    def from_ptr(arr,shape):
        return np.ctypeslib.as_array(arr,shape)


class float:  
    pass

class float_ptr:
    pointer = ctypes.POINTER(ctypes.c_float)

    def to_ptr(arr:np.array):
        return arr.ctypes.data_as(float_ptr.pointer)
    
    def from_ptr(arr,shape):
        return np.ctypeslib.as_array(arr,shape)


class py2C_dtypes():
    py_dtypes = {type(int()):"int",
              type(float()):"double",
              type(str()):"char*",
              type(double()):"double",
              type(double_ptr()):"double*",
              type(float()): "float",
              type(float_ptr()):"float*",
    }

    C_dtypes = {
            type(int()):ctypes.c_int,
            type(float()):ctypes.c_double,
            type(str()):ctypes.c_char_p,
            type(double()):ctypes.c_double,
            type(double_ptr()):ctypes.POINTER(ctypes.c_double),
            type(float()): ctypes.c_float,
            type(float_ptr()):ctypes.POINTER(ctypes.c_float),
    }
