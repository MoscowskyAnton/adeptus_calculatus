#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from pairing_core import PairingTable, PairingGame

def noise_em(table, num_elements, min_err, max_err):
    
    elements_indexes = table.get_random_indexes(num_elements)
    noised_table = table.scores.copy()
    for ei in elements_indexes:
        err = np.random.randint(min_err, max_err)
        noised_table[ei] += err
        if noised_table[ei] > 20:
            noised_table[ei] = 20
        elif noised_table[ei] < 0:
            noised_table[ei] = 0
    noise = noised_table - table.scores
    noise_p = np.sum(noise[noise >=0])
    noise_n = np.sum(noise[noise <0])
    return noised_table, noise_p, noise_n

if __name__ == '__main__':
    
    M = 500
    NOISED_ELEMENTS = 8
    MIN_NOISE = -10
    MAX_NOISE = 10
    
    real_scores = []
    noised_scores = []
    noises_pos = []
    noises_neg = []
    
    for m in range(M):
        # gen data 
        pt = PairingTable(np.random.randint(0,21,(4,4)))
        print(pt)
        pg = PairingGame(pt)
        
        # get real score
        pg.play_optimal_way()
        real_score = pg.get_score()
        real_scores.append(real_score)
    
        # noise em
        pg.PT.scores, noise_p, noise_n = noise_em(pg.PT, NOISED_ELEMENTS, MIN_NOISE, MAX_NOISE)
        pg.reset()
        print(pg.PT)
        noises_pos.append(noise_p)
        noises_neg.append(noise_n)
        
        # get noised score
        pg.play_optimal_way()
        noised_score = pg.get_score()
        
        noised_scores.append(noised_score)
        
    diff = np.array(noised_scores) - np.array(real_scores)
    #plt.plot(noises_neg, diff, '*')
    #plt.plot(noises_pos, diff, '*')
    noises_all = np.array(noises_neg)+np.array(noises_pos)
    plt.plot(noises_all, diff, '*')
    #for i, pos in enumerate(noises_pos):
        #plt.text(noises_all[i], diff[i], "{}/{}".format(pos, noises_neg[i]))
    
    plt.xlabel('Noise')
    plt.ylabel('Score diff')
    plt.grid()
    plt.title('Score change due to noise value')
    #print(real_scores, noised_scores)
    plt.show()
    
        
