#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

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

# stats

def to_wound(strength, toughness):
    roll = d6()
    if( strength == toughness ):
        if roll >= 4:
            return True
        else:
            return False
    elif( strength >= toughness *2 ):
        if roll >= 2:
            return True
        else:
            return False
    elif( toughness >= strength * 2):
        if roll >= 6:
            return True
        else:
            return False
    elif( toughness > strength ):
        if roll >= 5:
            return True
        else:
            return False
    else: # strength > toughness
        if roll >= 3:
            return True
        else:
            return False
            
# plot
def boxplot( data, ax, labels, color = 'r', rotation  = 0):
    means = np.mean(data, axis=1)
    print(means)
    bp = ax.boxplot(data, usermedians = means, sym='.'+color)
    plt.setp(bp['medians'],color=color, linewidth=3)    
    plt.xticks(range(1,1+len(data)), labels, rotation = rotation)    


if __name__ == '__main__' :
    
    # here should be unit tests
    pure = 0
    rr_ones = 0
    for n in range(1000):
        pure += d6()
        rr_ones += d6rr()
    print(pure, rr_ones)
