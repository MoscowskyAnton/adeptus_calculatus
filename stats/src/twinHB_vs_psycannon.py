#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

import ac_core


if __name__ == '__main__' :
    
    N = 10000
    twin_heavy_bolter_mean = []
    twin_heavy_bolter_q1 = []
    twin_heavy_bolter_q3 = []
    
    twin_psy_cannon_mean = []
    twin_psy_cannon_q1 = []
    twin_psy_cannon_q3 = []
    
    toughness = [4,5,6,7,8]
    
    for t in toughness:
        hb_d = []
        pc_d = []
        for i in range(N):
            # twin HB
            d = 0
            for j in range(6):
                if ac_core.d6rr(1) > 2:
                    if( ac_core.to_wound(5, t) ):
                        d += 2
            hb_d.append(d)
        
            # twin PC
            d = 0
            for j in range(8):
                if ac_core.d6rr(1) > 2:
                    if( ac_core.to_wound(7, t) ):
                        d += 1
            pc_d.append(d)
        
        twin_heavy_bolter_mean.append(np.mean(hb_d))
        twin_heavy_bolter_q1.append(np.quantile(hb_d, 0.25))
        twin_heavy_bolter_q3.append(np.quantile(hb_d, 0.75))
        
        twin_psy_cannon_mean.append(np.mean(pc_d))
        twin_psy_cannon_q1.append(np.quantile(pc_d, 0.25))
        twin_psy_cannon_q3.append(np.quantile(pc_d, 0.75))
        
    plt.xticks(toughness)
    plt.plot(toughness, twin_heavy_bolter_mean, label="twin_heavy_bolter")
    plt.fill_between(toughness, twin_heavy_bolter_q1, twin_heavy_bolter_q3, alpha = 0.1)
    
    plt.plot(toughness, twin_psy_cannon_mean, label="twin_psy_cannon")
    plt.fill_between(toughness, twin_psy_cannon_q1, twin_psy_cannon_q3, alpha = 0.1)
    plt.legend()
    plt.grid()
    plt.xlabel("Target toughness")
    plt.ylabel("Suffered damage if fail all saves")
    plt.title("Twin heavy bolter vs twin psycannon")
    plt.show()
    
    
