import os
import ctypes
import inspect
import re

#find variable x = re.findall("\w+\s*=\s*\w+", txt)

class var():
    def __init__(self):
        self.type = ''
        
        self.val = None
        self.name = ''

class Globals():
    def __init__(self):
        self.vars = {}

    def get_var(self,name):
        return self.vars[name]
    
    def set_var(self,name,dtype='',value=None):
        v = var()
        v.dtype = dtype
        v.value = value
        self.vars[name] = v

def test_func():
    x = 0
    y = 1
    for i in range(2,10,3):
        print('hello world')
        print("Hi")
        if i%2 == 0:
            x+=i
        y+=i
    return 0

def script_phraser(func):
    code = inspect.getsource(func)
    

script_phraser(test_func)