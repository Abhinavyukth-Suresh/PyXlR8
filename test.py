from pyXLR8 import py2C_dlib, Structure
from pyXLR8 import double_ptr, double
from ctypes import c_int,POINTER,byref,pointer
import numpy as np

def f(x:int,y:int)->int:
    """
    int sum = 0;
    sum += x+ y;
    return sum;
    """

class S(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int)]
    typedef = True
    pointer = True

def p(X:S)->S:
    """
    int a,b;
    a=5;b=5;
    //struct S s = {X->x+a,X->y+b};//creates local variable -> cannot return address
    struct S* s = malloc(sizeof(S));
    s->x = X->x+a;
    s->y = X->y+b;
    X->x =  256;
    return s;
    """

def array(arr:double_ptr,n:int)->double:
    """
    double sum = 0;
    for(int i=0;i<n;i++){
        sum+=arr[i];
    }
    return sum;
    """


print("Testing ..")
print("including Headers ..")
py2C_dlib.C_Foregin_GlobalSection(headers=["#include<stdio.h>","#include<stdlib.h>"])
# py2C_dlib.Compile_C_ForeginFunc(f)
print("generating structs ..")
py2C_dlib.C_Foregin_GlobalSection(data="typedef struct S{int x; int y;}S;")
print("building simple functions ..")
py2C_dlib.C_ForeginFunc(p)
print("functions with arrays ..")
py2C_dlib.C_ForeginFunc(array)
print("compiling and adding to global namespace ..")
py2C_dlib.compile(_name_space_=globals(),write_func_def=False,flags=["-O3","-ffast-math","-funroll-all-loops"])


K = S(4,4)
k2 = p(byref(K))
import ctypes
k = k2.contents
#print(9==k.x and 9==k.y)
a = double_ptr.to_ptr(np.zeros((20,)).astype(float))
print("testing ...")
#print(array(a,20))
#A = double_ptr.from_ptr(ret,shape=(N,))
