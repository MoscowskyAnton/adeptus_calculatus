#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

import ac_core


def weapon_eff(N, shots, bs, S, T, ap, sv, D):
    values = []        
    for i in range(N):
        # hits
        hits = 0
        for s in range(shots):
            if ac_core.d6() >= bs:
                hits+=1
        # wounds
        wounds = 0
        for h in range(hits):
            if( ac_core.to_wound(S, T) ):
                wounds +=1
        
        # saves
        failed = 0
        for w in range(wounds):
            if ac_core.d6() < sv - ap:
                failed +=1
        
        # damage
        damage = 0
        for f in range(failed):
            if callable(D):
                damage += D()
            else:
                damage += D
                
        values.append(damage)
            
    return np.mean(values), np.quantile(values, 0.25), np.quantile(values, 0.75)

if __name__ == '__main__' :
    
    N = 50000
    
    pl_m = []
    pl_q1 = []
    pl_q3 = []
    
    pc_m = []
    pc_q1 = []
    pc_q3 = []
    
    toughness = [4,5,6,7]
    for t in toughness:
        m, q1, q3 = weapon_eff(N, 6, 3, 4, t, 0, 3, ac_core.d3)
        pl_m.append( m )
        pl_q1.append( q1 )
        pl_q3.append( q3 )
        
        m, q1, q3 = weapon_eff(N, 4, 3, 7, t, -1, 3, 1)
        pc_m.append( m )
        pc_q1.append( q1 )
        pc_q3.append( q3 )
        
    plt.xticks(toughness)
    plt.plot(toughness, pl_m, label="psylancer")
    #plt.fill_between(toughness, pl_q1, pl_q3, alpha = 0.1)
    
    plt.plot(toughness, pc_m, label="psycannon")
    #plt.fill_between(toughness, pc_q1, pc_q3, alpha = 0.1)
    plt.legend()
    plt.grid()
    plt.xlabel("Target toughness")
    plt.ylabel("Suffered damage")
    plt.title("Psylancer vs psycannon")
    plt.show()
        
    
    

