#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np


def boxplots(data, ax, labels, color = 'r', rotation  = 0):
    means = np.mean(data, axis=1)
    print(means)
    bp = ax.boxplot(data, usermedians = means, sym='.'+color)
    plt.setp(bp['medians'],color=color, linewidth=3)    
    plt.xticks(range(1,1+len(data)), labels, rotation = rotation) 
    
    
def violinplots(data, ax, labels, rotation = 0, add_text = False):
    
    vp = ax.violinplot(data, showmeans = True, showextrema = True)
    if add_text:
        for i, d in enumerate(data):
            m = np.mean(d)
            plt.text(i+1, m*1.05, f"{round(m, 2)}", ha = 'right')
    
    plt.xticks(range(1,1+len(data)), labels, rotation = rotation) 
    ax.grid()


def plot_series(list_of_data_of_data, ax, labels, ticks, rotation = 0, add_cmp_text_on_data = -1):
    
    if add_cmp_text_on_data != -1:
        MEANS = []
        
    for data_of_data, label in zip(list_of_data_of_data, labels):
        
        means = []
        stds = []
        for data in data_of_data:
            means.append(np.mean(data))
            stds.append(np.std(data))          
        if add_cmp_text_on_data != -1:
            MEANS.append(means)
        
        means = np.array(means)
        stds = np.array(stds)
        
        plt.plot(range(len(data_of_data)), means ,marker='o', linestyle='-', label = label)
        plt.fill_between(range(len(data_of_data)), means - stds, means + stds, alpha = 0.3)
        
    if add_cmp_text_on_data != -1:
        for i, means in enumerate(MEANS):
            if i != add_cmp_text_on_data:
                for j, (m0, m) in enumerate(zip(MEANS[add_cmp_text_on_data], means)):
                    add = (m-m0)/m0*100
                    plt.text(j, m, f'{"+" if add >=0 else ""}{round(add, 1)}%')
        
    plt.xticks(range(len(data_of_data)), ticks, rotation = rotation) 
    plt.legend()
        
        
    
