import numpy as np
import ctypes
import os,sys
from pyXLR8.py2C_dtypes import *

class py2C_DIRS:
    COMPILER_CACHE_DIR = "__cache__"

class py2C_dlib():
    HEADERS = []
    FUNC_DEFS = []
    GLOBALS = []

    Fcount = 0
    FUNC_NAME_MAP = {} #maps py_func_name to cdll_func_name
    FUNC_MAP = {} #maps to cdll function after compilation
    FUNC_ATTR = {}

    PAGE_COUNTS = 0
    compiler_flags = {"-shared", "-fPIC"}
    namespace = {}
    DLLs = []
    
    def CompileGlobalSection(**kwargs):
        """Compile code to be put in global namespace"""
        if "headers" in kwargs:
             if type(kwargs["headers"])!=type(list()):
                  raise TypeError("headers must be list [header1, header2 ... ]")
             py2C_dlib.GLOBALS.append("\n".join(kwargs["headers"]))
        if "data" in kwargs:
             if type(kwargs["data"]!=type(str())):
                  raise TypeError("data must be a string")
             py2C_dlib.GLOBALS.append(kwargs["data"])

    def Compile_C_ForeginFunc(func,**kwargs):
        """compiles python function with c doc strings"""
        #numpy arrays must be converted to pointer 
        # np.array -> double_ptr.to_ptr(array)
        # return pointer -> double_ptr.from_ptr(array,shape)

        PY_FUNC_NAME = func.__name__
        RETURN_TYPE = py2C_dtypes.py_dtypes[func.__annotations__["return"]] if "return" in func.__annotations__ else "void"
        CDLL_FUNC_NAME =  f"CDLL_FOREGIN_FUNC_{py2C_dlib.Fcount}"
        func__annot__ = list(func.__annotations__)
        ARGS = {}
        Write_param = []
        CDLL_ARGS = []
        for i in range(func__annot__.__len__()):
                if func__annot__[i]=="return":continue
                arg = func__annot__[i]
                argtype = py2C_dtypes.py_dtypes[func.__annotations__[arg]]
                ARGS[arg] = argtype
                Write_param.append(f" {argtype} {arg}")
                CDLL_ARGS.append(py2C_dtypes.C_dtypes[func.__annotations__[arg]])
        CDLL_RESTYPE = py2C_dtypes.C_dtypes[func.__annotations__["return"]] if "return" in func.__annotations__ else None
        Write_param_str = ",".join(Write_param)
        func_data = f"//C code for {PY_FUNC_NAME}\n{RETURN_TYPE} {CDLL_FUNC_NAME} ({Write_param_str}){{\n {func.__doc__} }}\n"
        py2C_dlib.FUNC_DEFS.append(f"{RETURN_TYPE} {CDLL_FUNC_NAME} ({Write_param_str});")
        py2C_dlib.GLOBALS.append(func_data)
        py2C_dlib.FUNC_NAME_MAP[PY_FUNC_NAME] = CDLL_FUNC_NAME
        py2C_dlib.FUNC_ATTR[PY_FUNC_NAME] = (CDLL_ARGS,CDLL_RESTYPE)
        py2C_dlib.Fcount+=1

    def compile(_globals_,**kwargs):
        __flags__ = py2C_dlib.compiler_flags
        if "flags" in kwargs:
            cmp_flg = kwargs["flags"]
            try:
                __flags__ = __flags__.union(set(cmp_flg))
            except TypeError:
                 raise TypeError("flags must be an iterable, list or array")
        FLAGS = " ".join(__flags__)
        COMPILER = "gcc"
        if "compiler" in kwargs:
             COMPILER = kwargs["compiler"]

        headers = "\n".join(py2C_dlib.HEADERS)
        func_defs = "\n".join(py2C_dlib.FUNC_DEFS)
        globals_ = "\n".join(py2C_dlib.GLOBALS)
        write_data = f"{headers}\n{func_defs}\n{globals_}"
        FNAME = f"temp_dll_{py2C_dlib.PAGE_COUNTS}"
        CNAME = FNAME+".c"
        DLLNAME = FNAME+".so"

        cwd = os.getcwd()
        if not os.path.isdir(py2C_DIRS.COMPILER_CACHE_DIR):os.mkdir(py2C_DIRS.COMPILER_CACHE_DIR)
        os.chdir(py2C_DIRS.COMPILER_CACHE_DIR)
        with open(CNAME,"w") as w:w.write(write_data)
        compile_cmd = f"{COMPILER} {CNAME} -o {DLLNAME} {FLAGS}"
        status = os.system(compile_cmd)
        os.chdir(cwd)
        status = (1-status*2)
        if status<0:return status
        py2C_dlib.DLLs.append(DLLNAME)

        pyfnames = list(py2C_dlib.FUNC_NAME_MAP)
        cdll = ctypes.CDLL(f"{py2C_DIRS.COMPILER_CACHE_DIR}/./{DLLNAME}")
        py2C_dlib.namespace['cdll'] = cdll
        
        for i in range(pyfnames.__len__()):
            exec(f"{py2C_dlib.FUNC_NAME_MAP[pyfnames[i]]} = cdll.{py2C_dlib.FUNC_NAME_MAP[pyfnames[i]]}",py2C_dlib.namespace) 
            ARGTYPE,RESTYPE = py2C_dlib.FUNC_ATTR[pyfnames[i]]
            py2C_dlib.namespace[py2C_dlib.FUNC_NAME_MAP[pyfnames[i]]].argtypes = ARGTYPE
            if RESTYPE!=None:py2C_dlib.namespace[py2C_dlib.FUNC_NAME_MAP[pyfnames[i]]].restype = RESTYPE
            _globals_[pyfnames[i]] = py2C_dlib.namespace[py2C_dlib.FUNC_NAME_MAP[pyfnames[i]]]
        py2C_dlib.PAGE_COUNTS += 1
        return status