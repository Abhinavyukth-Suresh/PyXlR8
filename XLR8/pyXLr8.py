import inspect
import os
import re

INDENTATION = '    '

VARS = {}
FUNCS = {}

assignment = ["+=","-=","*=","/=","%=","&=","|=","^=","="]
assignment_map = {}

def test_func():
    x = 0
    for i in range(2,10,3):
        print('hello world')
        print("Hi")
        if i%2 == 0:
            x+=i
    return 0

########    COMPILING FUNCTIONS
def FOR(block):
    code = ''
    head = block.header
    iter_var = head.strip().split(' ')[1]
    iterator = head.strip().split(' ')[3]
    if "range" in iterator:
        if len(re.findall('(\(\d+\))',head))>0:
            start = str(0)
            end = re.findall('(\(\d+\))',head)[0][1:-1]
            skip = 1
            
        elif len(re.findall('(\(\d+,?\d*\))',head))>0:
            [start,end] =  re.findall('(\(\d+,?\d*\))',head)[0][1:-1].split(',')
            skip = 1

        elif len(re.findall('(\(\d+,?\d*,?\d*\))',head))>0:
            [start,end,skip] = re.findall('(\(\d+,*\d*,*\d*\))',head)[0][1:-1].split(',')

        code = code + f'for(int {iter_var}={start};{iter_var}<{end};{iter_var}+={skip})'
        code = code + '{'
        #others
        code = code + '}'  
    print(code)
    return code

def MAIN(block):
    code = block.code
    lines = code.split('\n')
    for i in range(len(lines)):
        pass

    for i in range(len(lines)):
        lines[i]=lines[i].strip()
        #finding variables
        j =0 
        while j<len(assignment):
            if assignment[j] in lines[i]:
                s = re.split(assignment[j],)
        
def IF():
    pass


### BLOCKS OBJECT 
class Block_objects():
    def __init__(self,type_,code,header=''):
        self.type = type_
        self.code = code
        self.blocks = []
        self.header = header
        self.c_code = ''
        self.VAR = {}
    
    def convert_to_C(self):
        if self.type == 'for':
            code = FOR(self)
        if self.type == 'main':
            code = MAIN(self)
        pass

    def print(self):
        print('printing ',self.header)
        for i in self.blocks:
            print('type :',i.type)
            print(i.code.strip())

#RECURSIVE ITERATION
def recursive_phraser(parent_block,master=False):
    VARS = parent_block.VAR.copy()
    
    code = parent_block.code
    code_lines = code.split('\n')
    if master:
        code_lines = code_lines[1:]
    BLOCK_KEY = ['for','def','with','while','if','elif','else']
    block_no = 0
    parent_block.blocks = [Block_objects('main','','main')]
    i=0
    last_block_ = False

    while i<len(code_lines):
        #blocks of code
        zero = code_lines[i].strip().split(' ')[0]
        if zero in BLOCK_KEY:
            if not last_block_:
                parent_block.blocks[-1].convert_to_C()
            last_block_ = True
            zero_indent = code_lines[i].rstrip().count(INDENTATION)
            block = Block_objects(zero,'',code_lines[i].strip())
            i+=1
            while code_lines[i].rstrip().count(INDENTATION)>zero_indent :
                block.code = block.code + '\n' + code_lines[i].rstrip()
                i+=1
                if  i>=len(code_lines):
                    break
            parent_block.blocks.append(block)
            recursive_phraser(block)     
            block.convert_to_C()
        else:
            if last_block_ :
                parent_block.blocks.append(Block_objects('main','','main'))
            last_block_ = False
            parent_block.blocks[-1].code = parent_block.blocks[-1].code + '\n' + code_lines[i].strip()
            i+=1

def script_phraser(func):
    code = inspect.getsource(func)
    Main_block = Block_objects('main',code,'main')
    recursive_phraser(Main_block,True)
    return 0
script_phraser(test_func) 