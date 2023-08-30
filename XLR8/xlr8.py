import numpy as np
import os
import regex
import inspect

INDENTATION = '    '

def test_func():
    x = 0
    for i in range(10):
        print('hello world')
        print("Hi")
        if i%2 == 0:
            x+=i
    return 0

def recursive_phraser(code):
    code_lines = code.split('\n')
    BLOCK_KEY = ['for','def','with','while','if','elif','else']
    blocks = [[]]
    i=1
    while i<len(code_lines)-1:
        zero = code_lines[i].strip().split(' ')[0]
        if zero in BLOCK_KEY:
            zero_indent = code_lines[i].rstrip().count(INDENTATION)
            blocks.append([])
            blocks[-1].append(code_lines[i].strip())
            i+=1
            while code_lines[i].rstrip().count(INDENTATION)>zero_indent:
                blocks[-1].append(code_lines[i].rstrip())
                i+=1
        else:
            blocks[-1].append(code_lines[i].strip())
            i+=1
    while [] in blocks:
        blocks.remove([])
    return blocks
    

def script_phraser(func):
    code = inspect.getsource(func)
    code_lines = code.split('\n')
    print(recursive_phraser(code))
    print(0/0)
    VARIABLES = {}
    FUNCTIONS = {}
    BLOCK_KEY = ['for','def','with','while','if','elif','else']
    blocks = [[]]
    i=1
    while i<len(code_lines)-1:
        zero = code_lines[i].strip().split(' ')[0]
        if zero in BLOCK_KEY:
            zero_indent = code_lines[i].rstrip().count(INDENTATION)
            blocks.append([])
            blocks[-1].append(code_lines[i].rstrip())
            i+=1
            while code_lines[i].rstrip().count(INDENTATION)>zero_indent:
                #probelem with nested loop -> convert to recursion
                blocks[-1].append(code_lines[i].rstrip())
                i+=1
        else:
            blocks[-1].append(code_lines[i].rstrip())
            i+=1
    while [] in blocks:
        blocks.remove([])
    return blocks

script_phraser(test_func) 