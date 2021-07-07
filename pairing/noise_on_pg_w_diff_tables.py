#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from pairing_core import PairingTable, PairingGame
import copy
from pairing_game_with_different_tables import PairingGame2


if __name__ == '__main__' :
    
    N = 5000
    
    #noises = []
    #score_diff = []
    
    noises = {}
    for n in range(N):
        pt = PairingTable(np.random.randint(0,21,(4,4)), teamA_player_names = ['Starrok', 'Aberrat', 'Strohkopf', 'Servius'])
        
        ri = np.random.randint(0,4)
        rj = np.random.randint(0,4)
        print('Fixed value: {} {}'.format(ri, rj))
        
        #noises.append(pt[ri,rj])
        if not pt[ri,rj] in noises:
            noises[pt[ri,rj]] = []
            
        
        pt2 = copy.deepcopy(pt)
        pt2.scores[ri,rj] = 0
        
        pg = PairingGame2(pt, pt2)
        
        pg.play_optimal_way()
        
        scA, scB = pg.get_score()
        
        #score_diff.append(scA - scB)
        noises[pt[ri,rj]].append(scA - scB)
    
    noises_mean = [np.mean(k) for k in noises.values()]
    
    
    plt.plot(list(noises.keys()), noises_mean, 'o')#, alpha = 0.1)
    #ax = plt.gca()
    #ax.boxplot(list(noises.values()))
    plt.title("Mean score change by noise value of one player")
    plt.xlabel('Mean score diff')
    plt.ylabel('Noise value')
    plt.grid()
    
    plt.show()
