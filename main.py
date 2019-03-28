# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:15:37 2018

@author: e0008730
"""
from importlib import reload
import enigma
reload(enigma)
from enigma import EnigmaMachine as Enigma
from enigma import ENIGMA_ORDER as LETTER_MAX

import mydecorator

#print(dir(mydecorator))

@mydecorator.ellapsed_time
def decipher(encoded : str):
    rotors = ['I','II','III']
    temp_enigma = Enigma(rotors, 'Reflector-A')
    
    for i in range(LETTER_MAX):
        for j in range(LETTER_MAX):
            for k in range(LETTER_MAX):
                init_pos = chr(65+i) + chr(65+j) + chr(65+k)
                temp_enigma.set_rotor(init_pos)
                decode = temp_enigma.encrypt(encode)
                if decode == message:
                    print(init_pos, decode)


rotors = ['I','II','III']
myenigma = Enigma(rotors, 'Reflector-A')

message = 'HELLOWORLD'
myenigma.set_rotor('AAA')
encode = myenigma.encrypt(message)
print(encode)
myenigma.set_rotor('AAA')
decode = myenigma.encrypt(encode)
print(decode)

decipher(encode)

