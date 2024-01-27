import sys

'''
from subprocess import Popen
import time

var = [11,2,3]
bar = 12
proc = Popen(['python', 'testfile2.py', str(var), str(bar)])
time.sleep(2)
print('hello world')

var = str(sys.argv[1])
bar = int(sys.argv[2])
'''
"""if 48 <= ord(char) <= 57:
                to_convert += char
            elif char in ',]':
                num_list.append(int(to_convert))
                to_convert = ''"""    

class Encoder():
    def __init__(self) -> None:
        pass

    @classmethod
    def coder(self, give_list: list) -> str:
        string = ''
        if not give_list:
            return '[]'
        for each in give_list:
            string += str(each) + ','
        return string


    @classmethod
    def decoder(self, list_string : str):
        num_list = []
        to_convert = ''
        if list_string == '[]':
            return num_list
        for char in list_string:  
            if char == ',':
                num_list.append(int(to_convert))
                to_convert = ''
            else: 
                to_convert += char                        
        return num_list
    
    def text_value_decoder(value: str) -> int:
        try: 
            int_value = round(float(value))
        except ValueError:
            print('Incorrect type. Enter an integer. Reverting to default value.')
            int_value = -40
        return int_value


    @classmethod
    def popen_generator(self, e_list : list, i_list : list, values_list: list[int], keye:str, keyi:str):
        cmd_list = ['python', 'exect.py']
        cmd_list.append(Encoder.coder(e_list))
        cmd_list.append(Encoder.coder(i_list))
        for each in values_list:
            cmd_list.append(each)
        cmd_list.append(keye)
        cmd_list.append(keyi)
        return cmd_list
    
    @classmethod
    def arg_acceptor(self):
        arguments = []
        for i in range(1, len(sys.argv)):
            arguments.append(sys.argv[i])
        return arguments
    
    #pppppppp

class CompartmentEncoder():
    def __init__(self) -> None:
        pass

    @classmethod
    def coder(self, give_list: list) -> str:
        string = ''
        if not give_list:
            return '[]'
        for each in give_list:
            string += str(each) + ','
        return string


    @classmethod
    def time_decoder(self, list_string : str):
        num_list = []
        to_convert = ''
        if list_string == '[]':
            return num_list
        for char in list_string:  
            if char == ',':
                if "." in to_convert:
                    num_list.append(float(to_convert))
                else:
                    num_list.append(int(to_convert))
                to_convert = ''
            else: 
                to_convert += char                        
        return num_list
    
    @classmethod
    def bool_decoder(self, list_string : str):
        num_list = []
        to_convert = ''
        if list_string == '[]':
            return num_list
        for char in list_string:  
            if char == ',':
                    num_list.append(int(to_convert))
                    to_convert = ''
            else: 
                to_convert += char   
        for i in range(4):
            num_list[i] /= 10000    
        num_list[2] *= 10          
        return num_list
    
    
    def text_value_decoder(value: str) -> int:
        try: 
            int_value = round(float(value))
        except ValueError:
            print('Incorrect type. Enter an integer. Reverting to default value.')
            int_value = -40
        return int_value
    
    @classmethod
    def popen_generator(self, times_list:list, strengths_list:list, cache:bool):
        cmd_list = ['python', 'exect_hh.py']
        for each in times_list:
            cmd_list.append(self.coder(each))
        for each in strengths_list:
            each = [int(every) for every in each]
            cmd_list.append(self.coder(each))
        cmd_list.append(str(cache))
        return cmd_list
    
    @classmethod
    def arg_acceptor(self):
        arguments = []
        for i in range(1, len(sys.argv)):
            arguments.append(sys.argv[i])
        return arguments
