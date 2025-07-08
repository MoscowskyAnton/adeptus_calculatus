#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt


def boxplots(data, ax, labels, color = 'r', rotation  = 0):
    means = np.mean(data, axis=1)
    print(means)
    bp = ax.boxplot(data, usermedians = means, sym='.'+color)
    plt.setp(bp['medians'],color=color, linewidth=3)    
    plt.xticks(range(1,1+len(data)), labels, rotation = rotation) 
    
def violinplots(data, ax, labels, rotation = 0):
    
    vp = ax.violinplot(data, showmeans = True, showextrema = True)
    plt.xticks(range(1,1+len(data)), labels, rotation = rotation) 
    ax.grid()
