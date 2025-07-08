#!/usr/bin/env python
# coding: utf-8

import numpy as np
import ac_core
import matplotlib.pyplot as plt

if __name__ == '__main__' :
    N = 100000
    
    exp_9 = []
    exp_11 = []
    
    for n in range(N):
        exp_9.append(ac_core.d6() + ac_core.d6())
        
        rolls = [ac_core.d6(), ac_core.d6(), ac_core.d6(), ac_core.d6()]
        exp_11.append(sum(sorted(rolls, reverse=True)[:2])) 
    
    prob_9 = np.sum(np.array(exp_9) >= 9)/N
    prob_11 = np.sum(np.array(exp_11) >= 11)/N
    print(f"Prob 9+: {prob_9}, Prob 11+: {prob_11}")
    
    
    fig1, ax1 = plt.subplots()
    #ax1.boxplot([exp_9, exp_11])            
    ac_core.boxplot([exp_9, exp_11], ax1, ["9+", "11+"], 'm')
    
    plt.plot(1, 9, 'om')
    plt.text(1, 9, f' 9+ {round(prob_9*100, 1)}%', ha = 'left')
    
    plt.plot(2, 11, 'om')
    plt.text(2, 11, f' 11+ {round(prob_11*100, 1)}%', ha = 'left')
    
    plt.grid()
    plt.title("9 on 2d6 vs 11 on 4d6 with 2 highest")
    plt.ylabel("Result")
    plt.xlabel("Roll")
    plt.show()
