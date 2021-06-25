#!/usr/bin/env python
# coding: utf-8

import numpy as np
import ac_core
import matplotlib.pyplot as plt

def do_seq( to_hit, to_wound, rr_hits = True):
    if rr_hits:        
        if ac_core.d6rr() >= to_hit:
            if ac_core.d6() >= to_wound:
                return 1
        return 0
    else:  # rr wounds
        if ac_core.d6() >= to_hit:
            if ac_core.d6rr() >= to_wound:
                return 1
        return 0    

if __name__ == '__main__' :
    
    N = 1000
    
    to_hits = [2, 3, 4, 5, 6]
    to_wounds = [2, 3, 4, 5, 6]
    
    data = np.zeros((5,5,2)) # hit, wound, rr_hit\rr_wound
    
    for n in range(N):
        print('{}/{}'.format(n,N))
        for i, th in enumerate(to_hits):
            for j, tw in enumerate(to_wounds):
                data[i, j, 0] += do_seq(th, tw, True)
                data[i, j, 1] += do_seq(th, tw, False)
                
    diff = (data[:,:,0] - data[:,:,1])/N * 100
    print(diff)
            
    fig, ax = plt.subplots()
    
    plus_one = [2,3,4,5,6,7]
    
    ax.pcolormesh(plus_one, plus_one, -diff, cmap = plt.get_cmap('coolwarm'), shading = 'flat', vmin = -5, vmax = 5)
    
    for i in range(to_hits):
        for j in range(to_wounds):
            plt.text()
            
    
    plt.xticks([2.5,3.5,4.5,5.5,6.5], ['2+', '3+', '4+', '5+', '6+'])
    plt.yticks([2.5,3.5,4.5,5.5,6.5], ['2+', '3+', '4+', '5+', '6+'])
    
    plt.show()
            
