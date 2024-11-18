#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':


    df = pd.read_csv("AM.csv")
    
    df.drop(df.columns[0], axis=1, inplace=True)
    
    #print(df.head())
    
    player_len = df.shape[1]
    print(f"Total: {player_len} players")
    
    units = {}
    
    for column_name, column_data in df.items():
        flag = True
        for index, value in column_data.items():
            if isinstance(value, str):
                if flag:
                    if value == "CHARACTERS":
                        flag = False
                    continue                
                    
                if value.endswith('ints)'):
                    index = value.find('(')
                    unit_name = value[:index-1]
                    
                    if 'Char' in unit_name:
                        for i, char in enumerate(unit_name):
                            if char == ':':
                                unit_name = unit_name[i+2:]
                    
                    if unit_name[0].isdigit():
                        for i, char in enumerate(unit_name):
                            if char == 'x':
                                unit_name = unit_name[i+2:]
                            
                        
                    
                    #print()
                    if not unit_name in units:
                        units[unit_name] = 1
                    else:
                        units[unit_name] += 1
    
    
    
    units = dict(sorted(units.items(),  key=lambda item: item[1], reverse = True))
    print(units)
    
    epic_heroes = ['Gaunt’s Ghosts', 'Sly Marbo', 'Ursula Creed', 'Callidus Assassin', 'Canis Rex', '‘Iron Hand’ Straken', 'Lord Solar Leontus']
    
    battle_line = ['Cadian Shock Troops', 'Infantry Squad', 'Death Korps of Krieg', 'Catachan Jungle Fighters']
    
    
    colors = []
    for unit in units:
        if unit in epic_heroes:
            colors.append(plt.get_cmap('tab10', 10)(1))
        elif unit in battle_line:
            colors.append(plt.get_cmap('tab10', 10)(2))
        else:
            colors.append(plt.get_cmap('tab10', 10)(0))
    
    x = np.arange(len(units))
    
    
    ###    
    plt.figure('absolyte')
    
    plt.title("AM Absolute Units")
    
    plt.bar(x, units.values(), color = colors)
    
    for i, num in enumerate(units.values()):
        plt.text(i, num+1, f"{num}", ha = 'center')
        
    
    plt.xticks(x, units.keys(), rotation = 90)
    plt.grid()
    
    #plt.ylim(0, player_len)
    plt.tight_layout()
    
    plt.savefig("am_abs_units.png", dpi = 300, bbox_inches='tight')
    
    
    ###
    
    plt.figure('relative')
    
    plt.title("AM Relative Units")
    
    y = []
    for unit, num in units.items():
        if unit in battle_line:
            y.append(num / 6 / player_len)
        elif unit in epic_heroes:
            y.append(num / player_len)
        else:
            y.append(num / 3 / player_len)
    
    plt.bar(x, y, color = colors)
    
    #for i, num in enumerate(y):
        #plt.text(i, num+1, f"{num}", ha = 'center')
        
    
    plt.xticks(x, units.keys(), rotation = 90)
    plt.grid()
    
    #plt.ylim(0, 1)
    plt.tight_layout()
    
    plt.savefig("am_rel_units.png", dpi = 300, bbox_inches='tight')
    
    plt.show()
