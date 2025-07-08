#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import scipy.stats

def calc_E(population, q = 0.95):
    n = population.shape[0]
    t = scipy.stats.t.ppf(q=q,df=n-1)    
    s = np.std(population)    
    E = t*np.sqrt(s**2/n)
    return E

if __name__ == '__main__':
    
    # Participant,Miniature,5,4,3,2,1,Like,Comment,Author_comment,Repost,Views
    df = pd.read_csv('RainforgeData.csv')    
    
    # add total voices
    voices = df['5'].values + df['4'].values + df['3'].values + df['2'].values + df['1'].values
    df.insert(df.shape[1], "Voices", voices, True)
    
    # get scores
    SCORES = []
    for index, row in df.iterrows():
        #SCORES[index] = []
        SCORES.append([])
        for value in range(1,6):
            SCORES[index] += [value] * row[str(value)]
    #print(SCORES)            
    
    # calc mean
    means = []    
    for scores in SCORES:
        means.append(np.mean(scores))
    df.insert(df.shape[1], "Mean", means, True)
        
    df_sorted_mean = df.sort_values(by=['Mean'], ascending=False)
    #print(df_sorted_mean['Participant'])
    SCORES_sorted = copy.deepcopy(SCORES)
    i = 1
    for index, row in df_sorted_mean.iterrows():
        #print(f"{i} #{index+1} {row['Participant']} [{row['Miniature']}] {row['Mean']}")        
        SCORES_sorted[i-1] = SCORES[index]
        i+=1
            
    
    #
    # MAIN RESULTS
    #
    
    plt.figure('violins_mean_sorted')
    plt.violinplot(SCORES_sorted, showmedians = False, showmeans = True)
    #plt.xticks()
    
    Es = []
    for i, scores_sorted in enumerate(SCORES_sorted):
        E = calc_E(np.array(scores_sorted), q = 0.95) 
        mean = np.mean(scores_sorted)
                
        plt.errorbar(i+1, mean, yerr = E, color = 'green', lolims=True)
        plt.errorbar(i+1, mean, yerr = E, color = 'green', uplims=True)
        plt.plot(i+1, mean, '.k')
    
    
    def get_labels(df):
        labels = []
        for index, row in df.iterrows():
            labels.append(f"{df['Participant'][index]} \n[{df['Miniature'][index]}]")
        return labels
    
    labels = get_labels(df_sorted_mean)
    
    plt.xticks(range(1,1+len(SCORES)), labels, rotation = 30)    
    plt.grid()
    plt.title("Participants sorted be pure mean value")
    plt.ylabel('Score')
    
    #
    # ACTIVITY 
    #
    plt.figure('activity')
            
    
    comments_authorless = df['Comment'] - df['Author_comment']
    #print(comments_authorless)
    activity = df['Like'] + df['Comment'] - df['Author_comment'] + df['Repost']
    df.insert(df.shape[1], "Activity", activity, True)
    df.insert(df.shape[1], "Comments_authorless", comments_authorless, True)
    df_sorted_activity = df.sort_values(by=['Activity'], ascending=False)
    
    ax = plt.gca()
    #labels = []
    #for index, row in df_sorted_activity.iterrows():
        #labels.append(f"{df_sorted_activity['Participant'][index]} \n[{df_sorted_activity['Miniature'][index]}]")
    #print(labels)
    labels = get_labels(df_sorted_activity)
        
    
    bottom = np.zeros(len(df_sorted_activity))    
        
    for column in ['Like', 'Comments_authorless', 'Repost']:
        v = df_sorted_activity[column].values
        p = ax.bar(labels, v, 0.6, label = column, bottom = bottom)
        bottom += v
        
    plt.legend()
    plt.xticks(rotation=30)
    plt.grid()
    plt.legend()
    plt.ylabel('Activity (likes+comments(author less)+reposts)')
    plt.title('Participants sorted by activity')
        
    #
    # ACTIVITY DEVIDED BY VIEWS
    #
    
    plt.figure('relative_activity')
    relative_activity = df['Activity'] / df['Views']
    df.insert(df.shape[1], "Related_activity", relative_activity, True)
    df_sorted_rel_activity = df.sort_values(by=['Related_activity'], ascending=False)
    plt.plot(df_sorted_rel_activity['Related_activity'].values, 'ro')
    plt.plot(df_sorted_rel_activity['Related_activity'].values, 'r-')
    
    
    labels = get_labels(df_sorted_rel_activity)
    plt.xticks(ticks = np.arange(0, len(labels), 1), labels = labels, rotation=30)
    plt.grid()
    plt.title('Particpants sorted by relative activity')
    plt.ylabel('Relative activity ((likes+comments(al)+reposts)/views)')
    
    #
    # Views + reposts
    #
    plt.figure('dynamic views')
    
    plt.plot(df['Views'].values, 'ro')
    plt.plot(df['Views'].values, 'r:')    
    plt.title('Dynamic views')
    plt.grid()
    maxx = np.max(df['Views'].values)
    plt.plot([4.5, 4.5], [0, maxx], 'k-')
    plt.plot([10.5, 10.5], [0, maxx], 'k-')
    plt.text(1.5, maxx+30, 'Day1')
    plt.text(7, maxx+30, 'Day2')
    plt.text(13, maxx+30, 'Day3')
    labels = get_labels(df)
    arr = np.arange(0, len(labels), 1)
    plt.xticks(ticks = arr, labels = labels, rotation=30)
    max_rep = np.max(df['Repost'].values)
    plt.bar(x = arr, height = df['Repost'] * (maxx / max_rep))
    plt.title('Views and reposts in dynamic')
    plt.ylabel('Views and reposts * (max_views/max_reposts)')
    
    #
    # Views sorted and votes
    #
    
    plt.figure('sorted views')
    df_views_sorted = df.sort_values(by=['Views'], ascending=False)
    plt.plot(df_views_sorted['Views'].values, 'ro')
    plt.plot(df_views_sorted['Views'].values, 'r-')
    
    factor = np.max(df['Views']) / np.max(df['Voices'])
    
    plt.plot(df_views_sorted['Voices'].values * factor, 'go')
    plt.plot(df_views_sorted['Voices'].values * factor, 'g:')
    
    labels = get_labels(df_views_sorted)
    plt.xticks(ticks = np.arange(0, len(labels), 1), labels = labels, rotation=30)
    plt.grid()
    plt.title('Particpants sorted by views with factored voices')
    plt.ylabel('Views, voices * (max views\max voices)')
    
    #
    # NO ones
    #
    SCORES_no1 = []
    for index, row in df.iterrows():
        #SCORES[index] = []
        SCORES_no1.append([])
        for value in range(2,6):
            SCORES_no1[index] += [value] * row[str(value)]
    
    means_no1 = []    
    for scores in SCORES_no1:
        means_no1.append(np.mean(scores))
    df.insert(df.shape[1], "Mean_no1", means_no1, True)
    
    df_sorted_mean_no1 = df.sort_values(by=['Mean_no1'], ascending=False)
    
    SCORES_no1_sorted = copy.deepcopy(SCORES_no1)
    i = 1
    for index, row in df_sorted_mean_no1.iterrows():
        #print(f"{i} #{index+1} {row['Participant']} [{row['Miniature']}] {row['Mean']}")        
        SCORES_no1_sorted[i-1] = SCORES_no1[index]
        i+=1
    
    plt.figure('violins_mean_no1_sorted')
    plt.violinplot(SCORES_no1_sorted, showmedians = False, showmeans = True)
    #plt.xticks()
    
    Es = []
    for i, scores_sorted in enumerate(SCORES_no1_sorted):
        E = calc_E(np.array(scores_sorted), q = 0.95) 
        mean = np.mean(scores_sorted)
                
        plt.errorbar(i+1, mean, yerr = E, color = 'green', lolims=True)
        plt.errorbar(i+1, mean, yerr = E, color = 'green', uplims=True)
        plt.plot(i+1, mean, '.k')
    
    labels = get_labels(df_sorted_mean_no1)
    
    plt.xticks(range(1,1+len(SCORES_no1_sorted)), labels, rotation = 30)    
    plt.grid()
    plt.title("Participants sorted be mean (without 1) value")
    plt.ylabel('Score')

    plt.show()
