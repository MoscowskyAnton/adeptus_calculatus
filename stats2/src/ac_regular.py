#!/usr/bin/env python
# coding: utf-8

import numpy as np
import string

def d3(max_ = False):
    if max_:
        return 3
    return np.random.randint(1,4)

def d6(max_ = False):
    if max_:
        return 6
    return np.random.randint(1,7)

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
        if set(dst) > allowed_symbols:
            raise ValueError(f'AC_REGULAR.__init__: invalid string {reg}')
        # split by +
        self.parsed = []
        parts = dst.split('+')
        for part in parts:
            if part.isdigit():
                self.parsed.append(int(part))
            else:
                # (X)DY, Y: 3\6
                
                
        
        
    
if __name__ == '__main__' :
    
    
