# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:15:37 2018

@author: e0008730
"""
import sys

'a module to realize Enigma machine'

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
    _value = 0
    def __init__(self, value_input: int):
        self._value = value_input % ENIGMA_ORDER
    #arithmetic operations
    def __neg__(self):
        return EnigmaNum(ENIGMA_ORDER - self._value)
    def __add__(self, num):
        return EnigmaNum(self._value + num._value)
    def __sub__(self, num):
        return EnigmaNum(self._value - num._value)
    #to use dictionary
    def __eq__(self, num):
        return (self._value==num._value)
    def __cmp__(self,num):
        return (self.value - num._value)
    #must be defined to be used as key of dictionary
    def __hash__(self):
        return self._value
    #for print
    def __str__(self) -> str:
        return "{0}".format(self._value)
    
    def tochar(self):
        #ord('A') is 65
        return chr(65 + self._value)

#base class for rotors, reflectors and plugboards
#since they are all some kind of letter substitution
#here we use the class EnigmaNum instead of letters
class SubstitutionCipher:
    #for example, if the string is AECBDF
    #then the sub table turns A to A, B to E, C to C, D to B, E to D and F to F
    def __init__(self, sub_in_char : str):
        rotor_upper = sub_in_char.upper()
        if self._check_table_consistency(rotor_upper)==True:
            #ord('A') is 65
            #substitute table
            self._table  = {EnigmaNum(i) : EnigmaNum(ord(rotor_upper[i]) - 65) for i in range(ENIGMA_ORDER)}
        else:
            sys.exit("substitution table consistency issue")
    #substitude on EnigmaNum to another        
    def substitute(self, enigmanum : EnigmaNum) -> EnigmaNum:
        return self._table[enigmanum]

    def _check_table_consistency(self, sub_in_char : str) -> bool:
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
    def _check_table_consistency(self, sub_in_char : str) -> bool:
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
    def _check_table_consistency(self, sub_in_char : str) -> bool:
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
    def __init__(self, wire_table_in_char : str):
        SubstitutionCipher.__init__(self, wire_table_in_char)
        rotor_upper = wire_table_in_char.upper()
        #_table specify how to substitute before the reflector
        #_table_back specify how to substitute after the reflector
        self._table_back = {EnigmaNum(ord(rotor_upper[i]) - 65) : EnigmaNum(i) for i in range(ENIGMA_ORDER)}
        self.__pos = EnigmaNum(0)
        
    def set_position(self, enigmanum):
        self.__pos = enigmanum
    def show_position(self):
        return self.__pos
    #give an input, turn it into another number
    #core idea of ENIGMA
    #need double check
    def substitute(self, enigmanum : EnigmaNum) -> EnigmaNum:
        return self._table[enigmanum + self.__pos]
    def substitute_back(self, enigmanum):
        return self._table_back[enigmanum] - self.__pos
    #rotate the rotor, and return a bool value to determine whether to rotate next rotor
    def rotate(self):
        self.__pos = self.__pos + EnigmaNum(1)
        if self.__pos == EnigmaNum(0):
            return True
        else:
            return False
        


rotor_type = {}
rotor_type["IC"] = "DMTWSILRUYQNKFEJCAZBPGXOHV"
rotor_type["IIC"] = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
rotor_type["IIIC"] = "UQNTLSZFMREHDPXKIBVYGJCWOA"


rotor_type["Rocket-I"] = "JGDQOXUSCAMIFRVTPNEWKBLZYH"
rotor_type["Rocket-II"] = "NTZPSFBOKMWRCJDIVLAEYUXHGQ"
rotor_type["Rocket-III"] = "JVIUBHTCDYAKEQZPOSGXNRMWFL"
rotor_type["Rocket-ETW"] = "QWERTZUIOASDFGHJKPYXCVBNML"


rotor_type["I-K"] = "PEZUOHXSCVFMTBGLRINQJWAYDK"
rotor_type["II-K"] = "ZOUESYDKFWPCIQXHMVBLGNJRAT"
rotor_type["III-K"] = "EHRVXGAOBQUSIMZFLYNWKTPDJC"
rotor_type["ETW-K"] = "QWERTZUIOASDFGHJKPYXCVBNML"


rotor_type["I"] = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_type["II"] = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_type["III"] = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
rotor_type["IV"] = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
rotor_type["V"] = "VZBRGITYUPSDNHLXAWMJQOFECK"
rotor_type["VI"] = "JPGVOUMFYQBENHZRDKASXLICTW"
rotor_type["VII"] = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
rotor_type["VIII"] = "FKQHTLXOCBJSPDZRAMEWNIUYGV"

rotor_type["Beta"] = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
rotor_type["Gamma"] = "FSOKANUERHMBTIYCWLQPZXVGJD"

#UKW stands for the Umkehrwalze in German
reflector_type = {}
reflector_type["UKW"] = "QYHOGNECVPUZTFDJAXWMKISRBL"
reflector_type["UKW-K"] = "IMETCGFRAYSQBZXWLHKDVUPOJN"
reflector_type["Reflector-A"] = "EJMZALYXVBWFCRQUONTSPIKHGD"
reflector_type["Reflector-B"] = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
reflector_type["Reflector-C"] = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
reflector_type["Reflector-B-Thin"] = "ENKQAUYWJICOPBLMDXZVFTHRGS"
reflector_type["Reflector-C-Thin"] = "RDOBJNTKVEHMLFCWZAXGYIPSUQ"

class EnigmaMachine:
    #_rotors = []
    #_plugboard = PlugBoard('EJMZALYXVBWFCRQUONTSPIKHGD')
    #assign each rotor a type
    def __init__(self, rotor_type_used : list, ref_type_used : str):
        self._reflector = Reflector(reflector_type[ref_type_used])
        self._rotors = [Rotor(rotor_type[name]) for name in rotor_type_used]
        
#        #cause error
#        for type in rotor_type_used:
#            self._rotors.append(Rotor(rotor_type[type]))
    
    #the steps for encrypt and decrypt are the same
    def encrypt(self, input_message : str):        
        #encrypt a string
        output = ""
        for letter in input_message.upper():
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
            #rotate th rotors accordingly
            i = 0
            while(i < len(self._rotors) and self._rotors[i].rotate() ):
               i = i + 1
        return output
        
#        #alternative way of using map
#        #sometimes causes mysterious mistakes
#        kk = list(map(self._encrypt_char, input_message))
#        return ''.join(kk)
    
    def set_rotor(self, rotor_pos : str):
        #set positions of rotors
        if len(self._rotors) == len(rotor_pos):
            for i in range(len(rotor_pos)):
                self._rotors[i].set_position(chartoenig(rotor_pos[i]))
        else:
            #sys.exit("Number of rotors does not fit!!!\n")
            raise ValueError('Number of rotors does not fit')
    
    def _encrypt_char(self, char : str) -> str:
        #encrypt a single letter
        temp = chartoenig(char)
        #pass through rotors
        for rotor in self._rotors:
            temp = rotor.substitute(temp)
        #pass through reflector
        temp = self._reflector.substitute(temp)
        #pass rotors in reversed order
        for rotor in reversed(self._rotors):
            temp = rotor.substitute_back(temp)
        #rotate th rotors accordingly
        i = 0
        while(i < len(self._rotors) and self._rotors[i].rotate() ):
           i = i + 1
        return temp.tochar()

        
    
if __name__ == "__main__":
#    #test PlugBoard
#    plug = PlugBoard('EJMZALYXVBWFCRQUONTSPIKHGD')
#    print(plug.sub(EnigmaNum(6)))
#    
#    #test reflector
#    ref = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
#    print(ref.sub(EnigmaNum(6)))
      
    rotors = ['I','II','III']
    enigma = EnigmaMachine(rotors, 'Reflector-A')

    #message = 'myxgoodxfriendxforxthexsecondxtimexinxourxhistoryxaxbritishxprimexministerxhasxreturnedxfromxgermanyxbringxpeacexwithxhonours'
    message = 'HELLOWORLD'
    enigma.set_rotor('AAA')
    encode = enigma.encrypt(message)
    print(encode)
    enigma.set_rotor('AAA')
    decode = enigma.encrypt(encode)
    print(decode)
    
                
        
        
    enigma.set_rotor('AAA')
    out = ''
    for a in message:
        #print(enigma._encrypt_char(a))
        out = out + enigma._encrypt_char(a)
    print(out)