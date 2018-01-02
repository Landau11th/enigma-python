# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:15:37 2018

@author: e0008730
"""
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
    
    def __eq__(self, num):
        return (self.value==num.value)
    
    def __cmp__(self,num):
        return (self.value - num.value)
    
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
        



a = EnigmaNum(67)
b = EnigmaNum(16)
print(a-b)
print((a-b).tochar())

L = Rotor('DMTWSILRUYQNKFEJCAZBPGXOHV')
#print(L.proj)
print(L.proj[EnigmaNum(6)].tochar())