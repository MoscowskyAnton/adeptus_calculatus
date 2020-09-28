#!/usr/bin/env python
# coding: utf-8

import ac_core
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__' :
    
    N = 10000
    results_rr = np.zeros(4)
    results_a = np.zeros(4)
    for i in range(3,7):
        for n in range(N):
            rr = ac_core.d6rr(i-1)
            if rr >= i:
                results_rr[i-3] += 1            
            a = ac_core.d6()
            if a >= i-1:
                results_a[i-3] += 1            
                
    results_a /= N
    results_rr /= N
    
    plt.plot([3,4,5,6], results_a, 'o-', label="add_to_hit")
    plt.plot([3,4,5,6], results_rr, 'o-', label="reroll")
    plt.xticks([3,4,5,6],["3+","4+","5+","6+"])
    plt.legend()
    plt.title("Reroll vs add to hit")
    plt.xlabel("Requred roll")
    plt.ylabel("Success probability")
    plt.show()
            
            


