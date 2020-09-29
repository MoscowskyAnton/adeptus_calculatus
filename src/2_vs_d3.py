#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import ac_core

if __name__ == '__main__' :
    N = 100000
    
    wounds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    
    damage2 = np.zeros(len(wounds))
    damage_d3 = np.zeros(len(wounds))
    damage_d3_q1 = np.zeros(len(wounds))
    damage_d3_q3 = np.zeros(len(wounds))
    damage_d3_min = np.zeros(len(wounds))
    damage_d3_max = np.zeros(len(wounds))
    
    for i, w in enumerate(wounds):
        sw = np.floor_divide(w,2)
        if sw *2 != w:
            sw += 1
        damage2[i] = sw
        
        fs_all = []
        for n in range(N):
            mw = 0            
            fs = 0
            while(mw < w):
                mw += ac_core.d3()
                fs+=1
            fs_all.append(fs)
        damage_d3[i] = np.mean(fs_all)
        damage_d3_q1[i] = np.quantile(fs_all, 0.25)
        damage_d3_q3[i] = np.quantile(fs_all, 0.75)
        damage_d3_min[i] = np.min(fs_all)
        damage_d3_max[i] = np.max(fs_all)
            
    D2Wr_2 = np.mean(wounds/damage2)
    D2Wr_d3 = np.mean(wounds/damage_d3)
    print("2 sum {}".format(D2Wr_2))
    print("d3 sum {}".format(D2Wr_d3))
    
    text_params = {'family': 'sans-serif',
                   'fontweight': 'bold'}
    
    plt.text(10, 2.5, "W/D_2={:.2}".format(D2Wr_2), **text_params)
    plt.text(10, 2, "W/D_d3={:.2}".format(D2Wr_d3), **text_params)
    
    
    plt.errorbar(wounds, damage_d3, [-damage_d3_q1+damage_d3, damage_d3_q3-damage_d3], label="Damage d3", uplims=True, lolims=True, marker="o",zorder=0)    
    #plt.fill_between(wounds, damage_d3_q1, damage_d3_q3, alpha = "0.25")
    plt.plot(wounds, damage_d3_min, '+', label="Damage d3 min", color="#1f77b4")    
    plt.plot(wounds, damage_d3_max, 'x', label="Damage d3 max", color="#1f77b4")    
    
    plt.plot(wounds, damage2, '-o', label="Damage 2",zorder=1)    
    
    plt.xticks(wounds)
    plt.legend()
    plt.grid()
    plt.xlabel("Target wound amount")
    plt.ylabel("Requred failed saves to kill target")
    plt.title("Damage 2 vs d3")
    plt.show()
