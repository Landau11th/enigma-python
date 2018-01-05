# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:07:10 2018

@author: e0008730
"""

import time;
import datetime;
import types

#print(time.time())
#print(datetime.datetime.now())


def log(func : types.FunctionType):
    def wrapper(*args, **kw):
        print('call %s():' %func.__name__)
        return func(*args, **kw)
    return wrapper

def ellapsed_time(func : types.FunctionType):
    print('first layer of ellapsed_time')
    def wrapper(*args, **kw):
        print('second layer of ellapsed_time')
        t = time.time()
        result = func(*args, **kw)
        print('%s executed in %s ms' % (func.__name__, 1000.0*(time.time() - t)))
        return result
    return wrapper

@log
def current_time():
    print("current_time called at " + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    #return datetime.datetime.now()
    
@ellapsed_time
def something(dt):
    time.sleep(dt)
        

if __name__ == '__main__':
    
    f = current_time
    #print(f())
    f()
    
    print('declare f as something')
    f = something
    print('call f i.e. something')
    f(0.6)
    
#    print(f.__name__)
#    print(type([]))
#    print(type(current_time))