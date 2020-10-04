#!/usr/bin/env python
# coding: utf-8

import numpy as np
import ac_core
import matplotlib.pyplot as plt
    

if __name__ == '__main__' :
    N = 10000
    
    exp_2d6 = []
    exp_4d3 = []
    
    for n in range(N):
        exp_2d6.append(ac_core.d6() + ac_core.d6())
        exp_4d3.append(ac_core.d3() + ac_core.d3() + ac_core.d3() + ac_core.d3())
        
    
    fig1, ax1 = plt.subplots()
    ax1.boxplot([exp_2d6, exp_4d3])
    
    ac_core.boxplot([exp_2d6, exp_4d3], ax1, ["2d6", "4d3"], 'm')
    plt.grid()
    plt.title("2d6 vs 4d3")
    plt.ylabel("Result")
    plt.xlabel("Roll")
    plt.show()
