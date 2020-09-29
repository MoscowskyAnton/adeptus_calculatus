#!/usr/bin/env python
# coding: utf-8

import numpy as np


#  dice rolls
def d6():
    return np.random.randint(1,7)

def d6rr( value_to_rr = 1):
    roll = d6()
    if( roll <= value_to_rr):
        roll = d6()
    return roll

def d3():
    return np.random.randint(1,4)


if __name__ == '__main__' :
    pass
    # here should be unit tests
