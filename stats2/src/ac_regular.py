#!/usr/bin/env python
# coding: utf-8

import numpy as np
import string
import re
from functools import partial

def roll_d3(max_ = False):
    if max_:
        return 3
    return np.random.randint(1,4)

def roll_d6(max_ = False):
    if max_:
        return 6
    return np.random.randint(1,7)

def roll_ndx(n, f, max_ = False):
    r = 0
    for _ in range(n):
        r += f(max_)
    return r

'''
    This class parses input regular string like '2D6+3' to function that calculates value randomly
    
    Allowed symbols:
        0-9
        +
        D d
        space
    
    args:
        reg - input string
'''
class AC_REGULAR(object):
    allowed_symbols = set(string.digits + '+' + 'd')
    
    def __init__(self, reg):
        # remove spaces
        dst = reg.replace(" ", "")
        # to lower
        dst = dst.lower()
        # check allowed
        if set(dst) > AC_REGULAR.allowed_symbols:
            raise ValueError(f'AC_REGULAR.__init__: invalid string {reg}, allowed symbols are {AC_REGULAR.allowed_symbols}')
        # split by +
        self.parsed = []
        parts = dst.split('+')
        for part in parts:
            if part.isdigit():
                self.parsed.append(int(part))
            else:
                # (X)DY, Y: 3\6
                if re.match('([0-9]+)?d[3,6]', part):
                    res = part.split('d')
                    if res[0] == '':
                        num = 1
                    else:
                        num = int(res[0])
                    if res[1] == '3':
                        f = roll_d3
                    else: # must be 6
                        f = roll_d6
                    self.parsed.append(partial(roll_ndx, n = num, f = f))
                                            
                else:
                    raise ValueError(f'AC_REGULAR.__init__: invalid syntax! {part}')
                
        #print(self.parsed)
        
    def roll(self, max_ = False):
        result = 0
        for p in self.parsed:
            if isinstance(p, int):
                result += p
            else:
                result += p(max_ = max_)
        return result
                        
                            
if __name__ == '__main__' :
    
    a = AC_REGULAR('2d6+6')
    print(a.roll())
    print(a.roll())
    print(a.roll(True))
    
    
