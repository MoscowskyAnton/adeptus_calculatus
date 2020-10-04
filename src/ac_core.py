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

# plot
def boxplot( data, ax, labels, color ):
    means = np.mean(data, axis=1)
    print(means)
    bp = ax.boxplot(data, usermedians = means, sym='.'+color)
    plt.setp(bp['medians'],color=color, linewidth=3)    
    plt.xticks(range(1,1+len(data)), labels)    


if __name__ == '__main__' :
    pass
    # here should be unit tests
