#!/usr/bin/env python
# coding: utf-8

'''
+ Smite, 5wc (+1 each) d3, or d6 if 11+

+ CSM, Infernal Gaze, 5wc, 3d6 - each 4+ mortal
CSM, Gift of Chaos, 6wc, greater target toughnes, d3+3

DG, Plague Wind, 5wc, d6 for each model, 6+ mortal
DG, Curse of the Leper, 7wc, 7d6, mortal for each roll > target toughnes

+ TS, Doombolt, 9wc, d3 mortals
+ TS, TzeenchFirestorm, 7wc, 9d6, 6+ - mortal

+CD, Tz, Bolt of change, 8wc, d3

CD, Nu, Stream of Corruption, 5wc, d3 if models <10, 10+ - d6

CD, Slaan, cacophonic choir, 6wc, 2d6 (+2 if result >10) - Ld = mortals

BA, Bloodboil, wc6, 2d6 > toughnes - d3, 2d6 > 2*toughnes - 3

SM, Psychic Scourge, wc6, D6+Ld(9) > D6+Ld_opp - d3, if == 1

+DA, Mind Worm, wc6, 1 mortal
DA, Trephination, wc7, 2d6 (+2 if result >10) - Ld = mortals

GK, Inner Fire, wc5, d6*numberof result of psytest, for each 3+ - mortal
GK, Purge soul, wc5, d6+Ld(9) - d6+Ld = numbers of morlals

Inq, Castigation, wc6, 3d6 > Ld - d3 mortals

SW, Living Lighing, wc6, d3
SW, Murderous Hurracane, wc5, 6+ for each unit
SW, Jaws, wc7, 2d6 - Move = mortals

+IG, Psychic Maelstrom, wc7, 2+ 3+ 4+ 5+ 6+

+Tyr, Psychic Screem, wc5, d3

Orkz, da krunch, wc8, d6 for each unit, 6 - mortal, then 2d6 if 10+, roll again d6 for each anf 6 mortal

Eld, Mind War, wc7, d6+LD - d6_Ld = mortals
Eld, Executioner, wc7, d3, if model slain + d3

Harl, wc7, d3

+Innary, Gaze of Ynnead, wc6, d6: 1- mortal, 2-5 - d3, 6 - d6

Gen, Psionic Blast, wc5, 2d6 < Ld - 1 mortal, >= LD - d3
Gen, Mental Onslaught, wc6, d6+Ld > d6+Ld - mortal, repeat until 6 or =<
'''

import numpy as np
import ac_core
import matplotlib.pyplot as plt

def smite(wc = 5):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        if psi_test >= 11:
            damage = ac_core.d6()
        else:
            damage = ac_core.d3()
    return damage

def infernal_gaze(wc = 5):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        for i in range(3):
            if ac_core.d6() >= 4:
                damage+=1
    return damage

def doombolt(wc = 9):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        damage = ac_core.d3()
    return damage

def tzeench_firestorm(wc = 7):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        for i in range(9):
            if ac_core.d6() == 6:
                damage+=1
    return damage
        
        
def bolt_of_change(wc = 8):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        damage = ac_core.d3()
    return damage        

def psychic_maelstorm(wc = 7):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        for i in range(5):
            if( ac_core.d6() >= i+2):
                damage += 1
            else:
                break
    return damage
            
            
def psychic_scream(wc = 5):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        damage = ac_core.d3()
    return damage                    

def gaze_of_ynnead(wc = 6):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        r = ac_core.d6()
        if r == 1:
            damage = 1
        elif r ==  6:
            damage = ac_core.d6()
        else:
            damage = ac_core.d3()
    return damage                    

def mindworm(wc = 6):
    damage = 0
    psi_test = ac_core.d6() + ac_core.d6()
    if psi_test >= wc:
        damage = 1
    return damage

#
#
#
def test_power(power, N = 10000, wc = None):
    results = []
    if wc is not None:
        for n in range(N):        
            results.append(power(wc))
    else:
        for n in range(N):        
            results.append(power())
            
    return results


if __name__ == '__main__' :
    
    data = []
    data.append(test_power(smite))
    data.append(test_power(smite, wc = 6))
    data.append(test_power(smite, wc = 7))
    data.append(test_power(infernal_gaze))
    data.append(test_power(doombolt))
    data.append(test_power(tzeench_firestorm))
    data.append(test_power(bolt_of_change))
    data.append(test_power(psychic_maelstorm))
    data.append(test_power(psychic_scream))     
    data.append(test_power(gaze_of_ynnead))    
    data.append(test_power(mindworm))    
    
    
    fig1, ax1 = plt.subplots()
    ac_core.boxplot(data, ax1, ["smite I", "smite II", "smite III", "infernal_gaze", "doombolt", "tzeench_firestorm", "bolt_of_change", "psychic_maelstorm", "psychic_scream", "gaze_of_ynnead", "mindworm"], "r")
    plt.show()
    

