#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import ac_core


if __name__ == '__main__' :
    
    # heavy3 vs take aim in rf vs take aim not rf 
    # on kasrkins with 2x volleys, 1 sniper
    
    N = 100000
    
    #heavy3 = {'hits':0, 'mortals':0, 'auto_wounds':0}
    #take_aim_rf = {'hits':0, 'mortals':0, 'auto_wounds':0}
    #take_aim_not_rf = {'hits':0, 'mortals':0, 'auto_wounds':0}
    #nothing = {'hits':0, 'mortals':0, 'auto_wounds':0}
    
    lasgun_guys = 6
    volley_guys = 2
    
    heavy3 = {'lasguns_shots': lasgun_guys * 3,
              'volly_shots': volley_guys * 2
                  }
    
    
    for i in range(N):
        # h3
        lasguns_shots = 6 * 3
        
        
    
    
    
