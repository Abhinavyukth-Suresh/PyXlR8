from pyXLR8 import py2C_dlib 
from pyXLR8 import double_ptr
import numpy as np

def f(x:int,y:int)->int:
    """
    int sum = 0;
    sum += x+ y;
    return sum;
    """

def p():
    """
    printf("inside p\\n");
    """

def array(arr:double_ptr)->double_ptr:
    """
    for(int i=0;i<10;i++){
        arr[i]+=i;
    }
    return arr;
    """

py2C_dlib.CompileGlobalSection(headers=["#include<stdio.h>","#include<stdlib.h>"])
py2C_dlib.Compile_C_ForeginFunc(f)
py2C_dlib.Compile_C_ForeginFunc(p)
py2C_dlib.Compile_C_ForeginFunc(array)

py2C_dlib.compile(globals(),flags=["-O3","-ffast-math"])

a = double_ptr.to_ptr(np.zeros((20,)))
A = double_ptr.from_ptr(array(a),shape=(20,))
print(A)
