#!/usr/bin/env python
# coding: utf-8

import numpy as np
import ac_core
import matplotlib.pyplot as plt

def do_seq( to_hit, to_wound, rr_hits):
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
    
def do_seq_2( to_hit, to_wound):
    h = ac_core.d6()
    w = ac_core.d6()
    res = [0, 0, 0]
    if h >= to_hit:
        if w >= to_wound:
            res[2] = 1
        else:
            if w == 1:
                w = ac_core.d6()
                if w >= to_wound:
                    res[1] = 1
    elif h == 1:
        h = ac_core.d6()
        if h >= to_hit:
            res[0] = 1
    return res
        

if __name__ == '__main__' :
    
    N = 10000
    
    to_hits = [2, 3, 4, 5, 6]
    to_wounds = [2, 3, 4, 5, 6]
    #to_hits = [2]
    #to_wounds = [6]
    
    data = np.zeros((len(to_hits),len(to_wounds),3)) # hit, wound, (rr_hit, rr_wound, both)
    
    for n in range(N):
        #print('{}/{}'.format(n,N))
        for i, th in enumerate(to_hits):
            for j, tw in enumerate(to_wounds):
                #h = do_seq(th, tw, True)
                #w = do_seq(th, tw, False)
                #if h and w:
                    #data[i, j, 2] += 1
                #else:
                    #data[i, j, 0] += h
                    #data[i, j, 1] += w
                data[i,j,:] = data[i,j,:] + do_seq_2(th, tw)
                
    #diff = (data[:,:,0] - data[:,:,1])/N * 100
    #print(diff)
    #diff2 = data[:,:,0,:] - data[:,:,1,:]
    
    #print(data)
    data = data / N * 100
            
    fig, ax = plt.subplots()
    
    plus_one = [2, 3, 4, 5, 6, 7]
    
    diff = data[:,:,0] - data[:,:,1]
    print(data)
    
    maxv = max(np.max(diff),np.abs(np.min(diff)))*2
    ax.pcolormesh(plus_one, plus_one, -diff.T, cmap = plt.get_cmap('coolwarm'), shading = 'flat', vmin = -maxv, vmax = maxv)
    
    for i, vi in enumerate(to_hits):
        for j, vj in enumerate(to_wounds):
            text = "{:.1f}/{:.1f}/{:.1f}".format(data[i,j,0], data[i,j,2], data[i,j,1])
            
            plt.text(vi+0.5, vj+0.5, text, ha = 'center', va='center')
            
    
    plt.xticks([2.5,3.5,4.5,5.5,6.5], ['2+', '3+', '4+', '5+', '6+'])
    plt.yticks([2.5,3.5,4.5,5.5,6.5], ['2+', '3+', '4+', '5+', '6+'])
    
    plt.xlabel('to hit')
    plt.ylabel('to wound')
    plt.title('Reroll of ones for to hit vs for to wound')
    
    plt.show()
            
