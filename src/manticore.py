#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

import ac_core

def get_hits(shots, rr_ones = False):
    rr = 0
    if rr_ones:
        rr = 1
    hits = 0
    for s in range(shots):
        if ac_core.d6rr(rr) >= 4:
            hits+=1
    return hits
    

if __name__ == '__main__' :
    
    N = 10000
    
    
    manticores = {}
    manticores['regular'] = []
    manticores['rr_ones'] = []
    manticores['rr_one_die'] = []
    manticores['rr_two_dies'] = []
    manticores['rr_two_dies_and_ones'] = []
    manticores['rr_one_die_and_ones'] = []
        
    for n in range(N):
        shot1 = ac_core.d6()
        shot2 = ac_core.d6()
                
        manticores['regular'].append(get_hits(shot1 + shot2))
        
        manticores['rr_ones'].append(get_hits(shot1 + shot2, True))
        
        shots = shot1 + shot2
        if min(shot1, shot2) <= 3:
            shots = max(shot1, shot2) + ac_core.d6()
        manticores['rr_one_die'].append(get_hits(shots, False))
        
        manticores['rr_one_die_and_ones'].append(get_hits(shots, True))
        
        if shot1 + shot2 < 8:
            shot1 = ac_core.d6()
            shot2 = ac_core.d6()
            
        manticores['rr_two_dies'].append(get_hits(shot1 + shot2))
        
        manticores['rr_two_dies_and_ones'].append(get_hits(shot1 + shot2, True))
        
    manticores = {k: v for k, v in sorted(manticores.items(), key=lambda item: np.mean(item[1]))}    
    
    fig1, ax1 = plt.subplots()        
    ac_core.boxplot(list(manticores.values()), ax1, list(manticores.keys()))
    plt.grid()
    plt.title("Manticores")
    plt.ylabel("Hits")
    plt.xlabel("Type")
    fig1.autofmt_xdate()
    plt.show()
        
        
