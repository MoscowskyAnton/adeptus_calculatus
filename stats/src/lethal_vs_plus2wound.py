#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import ac_core


if __name__ == '__main__' :
        
    N = 100000
    
    to_hits = [2, 3, 4, 5]    
    full_rerolls = [True, False]    
    to_wounds = [2, 3, 4, 5, 6]
    
    for to_hit in to_hits:
        for full_reroll in full_rerolls:                        
            
            all_lethal_cnt = []
            all_plus_wound_cnt = []
            
            for to_wound in to_wounds:
                
                lethal_cnt = []
                plus_wound_cnt = []
                
                for n in range(N):
                    if full_reroll:
                        hit_roll = ac_core.d6rr(to_hit - 1)                        
                    else:
                        hit_roll = ac_core.d6rr(1)                        
                    
                    if hit_roll == 6:
                        lethal_cnt.append(1)
                    
                    if hit_roll >= to_hit:
                        
                        wound_roll = ac_core.d6()
                        
                        if hit_roll != 6:                            
                            if wound_roll >= to_wound:                            
                                lethal_cnt.append(1)
                            else:
                                lethal_cnt.append(0)
                        
                        if wound_roll == 0:
                            plus_wound_cnt.append(0)
                        elif wound_roll+1 >= to_wound:
                            plus_wound_cnt.append(1)
                        else:
                            plus_wound_cnt.append(0)
                    else:
                        plus_wound_cnt.append(0)
                        #if hit_roll != 6:                            
                        lethal_cnt.append(0)
                                                                        
                            
                all_lethal_cnt.append(lethal_cnt)
                all_plus_wound_cnt.append(plus_wound_cnt)
            
            #print([len(a) for a in all_lethal_cnt])
            #print([len(a) for a in all_plus_wound_cnt])
            
            name = f"lethal_vs_plus_wound_{to_hit}_{full_reroll}"
            plt.figure(name)
            plt.title(f"Scions Lethals vs Plus Wound\n (to hit={to_hit}), full reroll={full_reroll}")
            
            all_lethal_cnt = np.array(all_lethal_cnt)
            all_plus_wound_cnt = np.array(all_plus_wound_cnt)
            
            mean_lethals = np.mean(all_lethal_cnt, axis = 1)
            mean_plus_wound = np.mean(all_plus_wound_cnt, axis = 1) 
            
            std_lethals = np.std(all_lethal_cnt, axis = 1)
            std_plus_wound = np.std(all_plus_wound_cnt, axis = 1)             
            
            plt.plot(mean_lethals*100, label = "Lethals")
            plt.plot(mean_plus_wound*100, label = "Plus wound")
            
            alpha = 0.1
            plt.fill_between(range(0, len(to_wounds)), 100*(mean_lethals - std_lethals), 100*(mean_lethals + std_lethals), alpha = alpha)
            plt.fill_between(range(0, len(to_wounds)), 100*(mean_plus_wound - std_plus_wound), 100*(mean_plus_wound + std_plus_wound), alpha = alpha)
            
            
            plt.grid()
            labels = [f"{tw}+" for tw in to_wounds]
            plt.xticks(range(0, len(to_wounds)), labels)
            plt.xlabel("To wound roll")
            plt.ylabel("wounded %")
            plt.legend()
            plt.ylim(0, 100)
            
            plt.savefig(f"../pics/{name}.png")
    
    plt.show()
                    
                                
                        
                        
                        
                    
                        
                
                
        

    
