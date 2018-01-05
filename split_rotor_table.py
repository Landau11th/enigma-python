# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:15:37 2018

@author: e0008730
"""

import re

myfile = open('rotor table.txt')

for line in iter(myfile):
    #pcs = line.split(' ', '\t')
    pcs = re.split('\s|\t',line)
    if pcs[0] == 'Rotor':
        print('\n')
    else:
        for i in range(len(pcs)):
            if len(pcs[i])==26:
                name = '-'.join(pcs[:i])
                if name.startswith('Reflector'):
                    print('reflector_type["%s"] = "%s"' % (name, pcs[i]))
                else:
                    print('rotor_type["%s"] = "%s"' % (name, pcs[i]))

print('end')