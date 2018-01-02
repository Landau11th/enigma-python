# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:15:37 2018

@author: e0008730
"""
import sys

ENIGMA_ORDER = 26

class EnigmaNum(object):
    value = 0
    def __init__(self, value_input: int):
        self.value = value_input % ENIGMA_ORDER
     
    def __neg__(self):
        return EnigmaNum(ENIGMA_ORDER - self.value)
    
    def __add__(self, num):
        return EnigmaNum(self.value + num.value)
    
    def __sub__(self, num):
        return EnigmaNum(self.value - num.value)
    #to use dictionary
    def __eq__(self, num):
        return (self.value==num.value)
    
    def __cmp__(self,num):
        return (self.value - num.value)
    #must be defined to be used as key of dictionary
    def __hash__(self):
        return self.value
    
    def __str__(self) -> str:
        return "{0}".format(self.value)
    
    def tochar(self):
        #ord('A') is 65
        return chr(65 + self.value)

class Rotor:
    proj = {}
    def __init__(self, rotor_input: str):
        #the rotor_input should give a bijection of the field to itself 
        rotor_upper = rotor_input.upper()
        if len(rotor_input) != ENIGMA_ORDER:
            raise Exception("wrong length for rotor input")
        else:
            self.proj = {EnigmaNum(i): EnigmaNum(ord(rotor_upper[i]) - 65) for i in range(ENIGMA_ORDER)}


rotor_type = {}
rotor_type['Commercial_IC'  ] = 'DMTWSILRUYQNKFEJCAZBPGXOHV'
rotor_type['Commercial_IIC' ] = 'HQZGPJTMOBLNCIFDYAWVEUSRKX'
rotor_type['Commercial_IIIC'] = 'UQNTLSZFMREHDPXKIBVYGJCWOA'
 
class ENIGMA:
    rotors = []
    _rotor_num = 0
    def __init__(self, rotor_num : int, rotor_type_used : list):
        self._rotor_num = rotor_num
        if(rotor_num == len(rotor_type_used)):
            for type in rotor_type_used:
                self.rotors.append(Rotor(rotor_type[type]))
        else:
            sys.exit("rotor number does not fit!\n")
        
    def encrypt(self, rotor_pos, list_of_EnigmaNum):
        for letter in list_of_EnigmaNum:
            temp = letter
            for rotor in self.rotors:
                temp = rotor.proj[temp]
    
    def decrypt(self, rotor_pos, list_of_EnigmaNum):
        return 0

a = EnigmaNum(67)
b = EnigmaNum(16)
print(a-b)
print((a-b).tochar())


L = Rotor(rotor_type['Commercial_IIIC'])
#print(L.proj)
print(L.proj[EnigmaNum(25)].tochar())