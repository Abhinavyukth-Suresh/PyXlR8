import re
import os
import inspect

INDENTATION = '    '

func_name = "func" 
MAP = f"""
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int {func_name}()
"""
MAP = MAP + "{"


def get_type(value):
    if "'" in value :
        return string(value.split("'")[1])
    elif '"' in value:
        return string(value.split('"')[1])
    elif "." in value:
        return Float(value)
    elif value in default_func:
        pass
    else:
        try:
            int(value)
            return Int(value)
        except:
            return string('')

class Printf():
    def __init__(self,line):
        self.line = line
    
    def get_datas(self):
        line = self.line
        datas = []
        str = ''
        i=0
        isstr = False
        while i<len(line):
            if line[i]=='"':
                str = str + '"'
                i+=1
                while line[i]!='"':
                    str = str+line[i]
                    i+=1
                i+=1
                str = str + '"'
                datas.append(str)
                str = ''
                
            if (line[i]==','):
                datas.append(str)
                str = ''
                i+=1

            if len(line)>i:
                str =  str + line[i]
                i+=1
                if len(line)==i:
                    datas.append(str)
            else:
                datas.append(str)
                str = ''
                
        print(datas)
        dt = [get_type(i) for i in datas]
        return dt

    def get_code(self):
        print("line",self.line)
        dt = self.get_datas()
        
        
        
        return ''
default_func = {"print":Printf}

############   DEFINING DATATYPES   #######################
class datatypes():
    def __init__(self,type_):
        self.type = type_ 
        self.value = None

class string(datatypes):
    def __init__(self,value=''):
        super().__init__('string')
        self.value = value

    def concat(self,str1,str2):
        pass

    def printfy(self):
        return "%s"
    
class Int(datatypes):
    def __init__(self, value):
        super().__init__("int")
        self.value=value
    
    def printfy(self):
        return "%d"

class Float(datatypes):
    def __init__(self, value):
        super().__init__("double")
        self.value=value   

    def printfy(self):
        return "%f"

class Funcs(datatypes):
    def __init__(self, name):
        super().__init__('')
        self.name = name
    
############   DEFINING BLOCKS   #######################

class Block():
    def __init__(self,type_,code,header=''):
        self.type = type_
        self.code = code
        self.blocks = []
        self.header = header
        self.VARS = {} 
        self.FUNCS = {}
    
    def convert_to_C():
        raise NotImplementedError
    
    def print(self):
        print('printing ',self.header)
        for i in self.blocks:
            print('type :',i.type)
            print(i.code.strip())

    def recursive_parsing(self,VAR={}):
        for i in self.blocks:
            VAR = i.recursive_parsing(VAR)
        return VAR

class For(Block):
    def __init__(self,code,header=''):
        super().__init__('for',code,header)
    
    def convert_to_C(self):
        pass

    def recursive_parsing(self,VAR={}):
        global MAP
        head = self.header
        iter_var = head.strip().split(' ')[1]
        iterator = head.strip().split(' ')[3]
        VAR[iter_var] = Int(iter_var)
        code = ''
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
            for i in self.blocks:
                VAR = i.recursive_parsing(VAR)
            code = code + '}\n' 
        MAP = MAP + code 
        return {}

class Main(Block):
    def __init__(self,code,header):
        super().__init__('main',code,header='')
    
    def convert_to_C(self):
        codeline = self.code.split('\n')
        n_line = len(codeline)
        for i in range(n_line):
            print(codeline[i])

    def get_type(self,value):
        if "'" in value :
            return string(value.split("'")[1])
        elif '"' in value:
            return string(value.split('"')[1])
        elif "." in value:
            return Float(value)
        elif value in self.FUNCS:
            pass
        elif value in default_func:
            pass
        else:
            try:
                int(value)
                return Int(value)
            except:
                print("error")
                exit()


    def recursive_parsing(self,VAR={}):
        global MAP
        codeline = self.code.split('\n')
        n_line = len(codeline)
        for i in range(n_line):
            s=re.search('\w+\s*=\s*\w+',codeline[i])
            if s:
                sp = re.split('=',codeline[i])
                VAR[sp[0].strip()]=self.get_type(sp[1].strip()) #sp[1].strip()
                MAP = MAP + VAR[sp[0].strip()].type +" "+ sp[0].strip() + "=" + sp[1].strip() + ";\n"
            s=re.search('\w+\(.*\)',codeline[i])
            if s:
                sp = re.split('\(.*\)',codeline[i])
                if sp[0] in default_func:
                    ss = re.search('\(.*\)',codeline[i])
                    param = codeline[i][ss.start():ss.end()]
                    func = default_func[sp[0]](param[1:-1])
                    MAP = MAP + func.get_code() + "\n"
                #print("func",sp[0])
            pass
        for i in self.blocks:
            VAR = i.recursive_parsing(VAR=VAR)
        return VAR

class If(Block):
    def __init__(self,code,header):
        super().__init__('if',code,header='')
    
    def convert_to_C(self):
        pass

class GlobalBlock(Block):
    def __init__(self,code,header):
        super().__init__('global',code,header)
    
    def convert_to_C(self):
        for i in self.blocks:
            i.convert_to_C()
            
block_types  = {'main':Main,'for':For,'while':None,
                'if':If,'elif':None,'else':None,
                'with':None,'def':None}

def assign_block(type_,code,header=''):
    block = block_types[type_](code=code,header=header)
    return block

######## TESTING 

def test_func():
    x = 0
    y= 1
    for i in range(2,10,3):
        print("hello world",5)
        print("Hi","worlds")
        if i%2 == 0:
            x+=i
    return 0

def recursive_phraser(parent_block,master=False):
    code = parent_block.code
    code_lines = code.split('\n')
    if master:
        code_lines = code_lines[1:]
    BLOCK_KEY = list(block_types)
    block_no = 0
    parent_block.blocks = [Main('','')]
    i=0
    last_block_ = False

    while i<len(code_lines):
        zero = code_lines[i].strip().split(' ')[0]
        if zero in BLOCK_KEY:
            if not last_block_:
                #parent_block.blocks[-1].convert_to_C()
                pass
            last_block_ = True
            zero_indent = code_lines[i].rstrip().count(INDENTATION)
            block = assign_block(zero,'',header=code_lines[i].strip())
            i+=1
            while code_lines[i].rstrip().count(INDENTATION)>zero_indent :
                block.code = block.code + '\n' + code_lines[i].rstrip()
                i+=1
                if  i>=len(code_lines):
                    break
            
            parent_block.blocks.append(block)
            recursive_phraser(block) 
        else:
            if last_block_ :
                parent_block.blocks.append(Main('',''))
            last_block_ = False
            parent_block.blocks[-1].code = parent_block.blocks[-1].code + '\n' + code_lines[i].strip()
            i+=1

def script_phraser(func):
    global MAP
    code = inspect.getsource(func)
    Main_block = GlobalBlock(code,'main')
    recursive_phraser(Main_block,True)
    Main_block.recursive_parsing()
    MAP = MAP + "}"
    return 0
script_phraser(test_func) 

print(MAP)