#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from pairing_core import PairingTable, PairingGame


if __name__ == '__main__':
    
    M = 20
    N = 20
    optimal_scores = []
    random_scores = []
    random_scores2 = []
    mean_score = []
    for m in range(M):
        pt = PairingTable(np.random.randint(0,21,(4,4)))
        pg = PairingGame(pt)
        
        mean_score.append(pt.mean())
        print(pg.PT)
        print('TEAM A mean score = {}'.format(pg.PT.mean()))
        
        pg.play_optimal_way()
        score_optimal = pg.get_score()
        pg.print_results()
        optimal_scores.append(score_optimal)
    
        scores_optimal_vs_random = []
        scores_random_vs_optimal = [] 
        for n in range(N):
            pg.reset()
            pg.play_random_vs_optimal()
            scores_optimal_vs_random.append(pg.get_score())
            #pg.print_results()
            pg.reset()
            pg.play_optimal_vs_random()
            scores_random_vs_optimal.append(pg.get_score())
            
        random_scores.append(scores_optimal_vs_random)
        random_scores2.append(scores_random_vs_optimal)
        
    #print(optimal_scores, random_scores)
    cmap = plt.get_cmap("tab10")
    plt.plot(optimal_scores,'-', color = cmap(0), label="Both teams optimal")
    plt.plot(mean_score, '-', label="Mean Team A value", color = cmap(1))
    l = "Team A random, team B optimal"
    for i, rs in enumerate(random_scores):
        plt.plot([i]*len(rs), rs,'.', label = l, color = cmap(2))
        l = None
    l = "Team A optimal, team B random"
    for i, rs in enumerate(random_scores2):
        plt.plot([i]*len(rs), rs,'.', label = l, color = cmap(3))
        l = None
    
    plt.title('Minimax vs random moves')
    plt.legend()
    plt.ylabel('game score')
    plt.xlabel('# exp')
    plt.grid()
    plt.show()
