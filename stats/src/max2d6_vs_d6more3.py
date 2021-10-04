#!/usr/bin/env python
# coding: utf-8

import numpy as np
import ac_core
import matplotlib.pyplot as plt
    

if __name__ == '__main__' :
    N = 1000000
    
    exp_max_2d6 = []
    exp_max_3_d6 = []
    exp_d6_rr1 = []
    
    for n in range(N):
        exp_max_2d6.append(max(ac_core.d6(), ac_core.d6()))
        exp_max_3_d6.append(max(ac_core.d6(), 3))
        exp_d6_rr1.append(ac_core.d6rr(1))
        
    
    fig1, ax1 = plt.subplots()
    #ax1.boxplot([exp_max_2d6, exp_max_3_d6])
    
    ac_core.boxplot([exp_max_2d6, exp_max_3_d6, exp_d6_rr1], ax1, ["max(2d6)", "d6 not less 3", "d6 reroll 1"], 'm')
    plt.grid()
    plt.title("Super-heavy guns")
    plt.ylabel("Result")
    plt.xlabel("Roll")
    plt.show()
