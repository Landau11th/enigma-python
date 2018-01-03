# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:15:37 2018

@author: e0008730
"""
import sys

#for enigma, the order of the additive group is 26
#be careful to change this value
ENIGMA_ORDER = 26

#turns a charactor to a EnigmaNum
def chartoenig(ch : str):
    return EnigmaNum(ord(ch) - ord('A'))

#EnigmaNum, i.e. an additive group of order 26
#this approach is more complicated, but more general in the sense of
#being extended to discrete field
class EnigmaNum(object):
    value = 0
    def __init__(self, value_input: int):
        self.value = value_input % ENIGMA_ORDER
    #arithmetic operations
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
    #for print
    def __str__(self) -> str:
        return "{0}".format(self.value)
    
    def tochar(self):
        #ord('A') is 65
        return chr(65 + self.value)

#base class for rotors, reflectors and plugboards
#since they are all some kind of letter substitution
#here we use the class EnigmaNum instead of letters
class SubstitutionCipher:
    #substitute table
    _table = {}
    #for example, if the string is AECBDF
    #then the sub table turns A to A, B to E, C to C, D to B, E to D and F to F
    def __init__(self, sub_in_char : str):
        rotor_upper = sub_in_char.upper()
        if self._check_table_consistency(rotor_upper)==True:
            #ord('A') is 65
            self._table  = {EnigmaNum(i) : EnigmaNum(ord(rotor_upper[i]) - 65) for i in range(ENIGMA_ORDER)}
        else:
            sys.exit("substitution table consistency issue")
    #substitude on EnigmaNum to another        
    def substitute(self, enigmanum : EnigmaNum) -> EnigmaNum:
        return self._table[enigmanum]

    def _check_table_consistency(self, sub_in_char : str):
        #for a substitution, we must guarantee that each letter appears only once
        temp_dict = {chr(ord('A')+i) : 0 for i in range(ENIGMA_ORDER)}
        for char in sub_in_char:
            temp_dict[char] += 1
        #count how many times a letter appears
        if len(temp_dict) == ENIGMA_ORDER:
            for key, value in temp_dict.items():
                if value >= 2:
                    print("duplicate "+key)
                    return False
            return True
        else:
            print("wrong input of substitution table")
            return False

#plugboard swap pair of letters
#in history the number of pairs is 4 to 10
#however the number of pairs is not restricted here
class PlugBoard(SubstitutionCipher):
    def __init__(self, sub_in_char : str):
        SubstitutionCipher.__init__(self, sub_in_char)
    def _check_table_consistency(self, sub_in_char : str):
        if super(PlugBoard, self)._check_table_consistency(sub_in_char) == False:
            return False
        else:
            temp_dict = {chr(ord('A')+i) : sub_in_char[i] for i in range(ENIGMA_ORDER)}
            for key, value in temp_dict.items():
                #swapping two letters twice means doing nothing
                if key != temp_dict[value]:
                    print(key+" and "+value+" are not swapped in plugboard")
                    return False
            return True

#reflector swap pair of letters
#in history the number of pairs 13
#however the number of pairs is not restricted here
#currently the reflector is the same with plugboard
#we may add rotation function to it later
class Reflector(SubstitutionCipher):
    def __init__(self, sub_in_char : str):
        SubstitutionCipher.__init__(self, sub_in_char)
    def _check_table_consistency(self, sub_in_char : str):
        if super(Reflector, self)._check_table_consistency(sub_in_char) == False:
            return False
        else:
            temp_dict = {chr(ord('A')+i) : sub_in_char[i] for i in range(ENIGMA_ORDER)}
            #swapping two letters twice means doing nothing
            for key, value in temp_dict.items():
                if key != temp_dict[value]:
                    print(key+" and "+value+" are not swapped in plugboard")
                    return False
            return True
         
#rotors could do any bijective mapping
#therefore a backward table is also needed
#rotation is the key feature of rotors
class Rotor(SubstitutionCipher):
    #_table specify how to substitute before the reflector
    #_table_back specify how to substitute after the reflector
    _table_back = {}
    _count = EnigmaNum(0)
    def __init__(self, wire_table_in_char : str):
        SubstitutionCipher.__init__(self, wire_table_in_char)
        rotor_upper = wire_table_in_char.upper()
        self._table_back = {EnigmaNum(ord(rotor_upper[i]) - 65) : EnigmaNum(i) for i in range(ENIGMA_ORDER)}
        
    def set_position(self, enigmanum):
        self._count = enigmanum
    def show_position(self):
        return self._count
    #give an input, turn it into another number
    #core idea of ENIGMA
    #need double check
    def substitute(self, enigmanum : EnigmaNum) -> EnigmaNum:
        return self._table[enigmanum + self._count]
    def substitute_back(self, enigmanum):
        return self._table_back[enigmanum] - self._count
    #rotate the rotor, and return a bool value to determine whether to rotate next rotor
    def rotate(self):
        self._count = self._count + EnigmaNum(1)
        if self._count == EnigmaNum(0):
            return True
        else:
            return False
        


rotor_type = {}
rotor_type['IC'  ] = 'DMTWSILRUYQNKFEJCAZBPGXOHV'
rotor_type['IIC' ] = 'HQZGPJTMOBLNCIFDYAWVEUSRKX'
rotor_type['IIIC'] = 'UQNTLSZFMREHDPXKIBVYGJCWOA'

#UKW stands for the Umkehrwalze in German
reflector_type = {}
reflector_type['UKW'] = 'QYHOGNECVPUZTFDJAXWMKISRBL'
reflector_type['UKW-K'] = 'IMETCGFRAYSQBZXWLHKDVUPOJN'
reflector_type['A'] = 'EJMZALYXVBWFCRQUONTSPIKHGD'
reflector_type['B'] = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
reflector_type['C'] = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
reflector_type['B_thin'] = 'ENKQAUYWJICOPBLMDXZVFTHRGS'
reflector_type['C_thin'] = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'

class EnigmaMachine:
    _rotors = []
    #_plugboard = PlugBoard('EJMZALYXVBWFCRQUONTSPIKHGD')
    #assign each rotor a type
    def __init__(self, rotor_type_used : list, ref_type_used : str):
        self._reflector = Reflector(reflector_type[ref_type_used])
        for type in rotor_type_used:
            self._rotors.append(Rotor(rotor_type[type]))
    
    #the steps for encrypt and decrypt are the same
    def encrypt(self, rotor_pos, list_of_EnigmaNum : str):
        #set positions of rotors
        if len(self._rotors) == len(rotor_pos):
            for i in range(len(rotor_pos)):
                self._rotors[i].set_position(chartoenig(rotor_pos[i]))
        else:
            sys.exit("Number of rotors does not fit!!!\n")   
        
        #encrypt a string
        output = ""
        for letter in list_of_EnigmaNum.upper():
            #encrypt a single letter
            temp = chartoenig(letter)
            #pass through rotors
            for rotor in self._rotors:
                temp = rotor.substitute(temp)
            #pass through reflector
            temp = self._reflector.substitute(temp)
            #pass rotors in reversed order
            for rotor in reversed(self._rotors):
                temp = rotor.substitute_back(temp)
            output = output + temp.tochar()
            #rotate th rotors
            i = 0
            while(i < len(self._rotors) and self._rotors[i].rotate() ):
               i = i + 1
        
        return output
                
    
if __name__ == "__main__":
#    #test PlugBoard
#    plug = PlugBoard('EJMZALYXVBWFCRQUONTSPIKHGD')
#    print(plug.sub(EnigmaNum(6)))
#    
#    #test reflector
#    ref = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
#    print(ref.sub(EnigmaNum(6)))
    
    rotors = ['IC','IIC','IIIC']
    enigma = EnigmaMachine(rotors, 'A')
    
    #message = 'myxgoodxfriendxforxthexsecondxtimexinxourxhistoryxaxbritishxprimexministerxhasxreturnedxfromxgermanyxbringxpeacexwithxhonours'
    message = 'helloworld'
    encode = enigma.encrypt('AAA',message)
    print(encode)
    decode = enigma.encrypt('AAA',encode)
    print(decode)