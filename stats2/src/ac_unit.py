#!/usr/bin/env python
# coding: utf-8
import ac_weapon
from enum import Enum, auto
import copy
import matplotlib.pyplot as plt
from ac_plot import violinplots
import numpy as np
import ac_regular

class AC_UNIT(object):            
    
    def __init__(self, movement, toughness, save, invul, wounds, leadership, oc, weapons = [], *args, **kwargs):
                
        
        # TODO: check values
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.invul = invul
        self.wounds = wounds
        self.leadership = leadership
        self.oc = oc                
                
        self.args_abilities = args
        self.kwargs_abilities = kwargs
        
        self.weapons = []
        self.add_weapons(weapons)
        
        
    def add_weapons(self, weapons):
        for wep in weapons:
            wc = copy.copy(wep)
            wc.args_abilities = wc.args_abilities + self.args_abilities
            wc.kwargs_abilities = {**wc.kwargs_abilities, **self.kwargs_abilities}
            self.weapons.append(wc)
            #print(wc.args_abilities)
    
    
    def attack_target(self, target, range_):
        
        total_damage = 0
        for weapon in self.weapons:
            total_damage += weapon.get_damage(target, range_)
            
        # NOTE: kostyl'
        if ac_weapon.AC_WEAPON.IGNORE_DAMAGE in target.kwargs_abilities:
            total_damage = max(0 ,total_damage - ac_regular.AC_REGULAR('d6').roll())
            
        return total_damage
            
    
    def mean_damage_target(self, target, range_, N):
        td = 0
        for i in range(N):
            td += self.attack_target(target, range_)
        return td / N
    
    def get_data_damage_target(self, target, range_, N):
        data = []
        for i in range(N):
            data.append(self.attack_target(target, range_))
        return data
        
    def get_success_percent_damage_on_target(self, target, data):
        success_data = np.where(np.array(data) >= target.wounds, 1, 0)
        cnt = np.count_nonzero(success_data)
        perc = cnt / len(data)
        return perc
    
if __name__ == '__main__':
    
    # weapons
    LasCannon = ac_weapon.AC_WEAPON(48, 1, 4, 12, 3, 'd6+1')
    MultiMelta = ac_weapon.AC_WEAPON(18, 2, 4, 9, 4, 'd6', MELTA = 2)
    HeavyStubber = ac_weapon.AC_WEAPON(36, 3, 4, 4, 0, 1, RAPID_FIRE = 3)
    DemolisherCannon = ac_weapon.AC_WEAPON(24, 'd6+3', 4, 14, 3, 'd6')
    HunterKillerMissile = ac_weapon.AC_WEAPON(48, 1, 4, 14, 3, 'd6')
    
    OpressorCannon = ac_weapon.AC_WEAPON(60, 'd6+3', 4, 12, 2, 3)
    CoaxialAutoCannon = ac_weapon.AC_WEAPON(48, 2, 3, 9, 1, 3)
    PulziverCannon = ac_weapon.AC_WEAPON(24, 'd6', 4, 9, 3, 3)
    MeltaGun = ac_weapon.AC_WEAPON(12, 1, 4, 9, 4, 'd6', MELTA = 2)
    
    # units
    LemanRussDemolisher = AC_UNIT(10, 11, 2, 0, 13, 7, 3, 
                                  [DemolisherCannon, 
                                   LasCannon, 
                                   MultiMelta, 
                                   MultiMelta, 
                                   HeavyStubber, 
                                   HunterKillerMissile
                                   ], 
                                  ac_weapon.AC_WEAPON.LETHAL_HITS, 
                                  #ac_weapon.AC_WEAPON.PLUS_BS
                                  #ac_weapon.AC_WEAPON.IN_COVER
                                  )
    
    RogalDornBattleTank = AC_UNIT(10, 12, 2, 0, 18, 7, 5, 
                                  [OpressorCannon, 
                                   CoaxialAutoCannon, 
                                   MultiMelta, 
                                   MultiMelta, 
                                   HeavyStubber, 
                                   HeavyStubber, 
                                   HeavyStubber, 
                                   PulziverCannon
                                   ], 
                                  ac_weapon.AC_WEAPON.LETHAL_HITS,
                                  #ac_weapon.AC_WEAPON.PLUS_BS
                                  #ac_weapon.AC_WEAPON.IN_COVER
                                  IGNORE_DAMAGE = 1
                                  )
    #RogalDornBattleTank = AC_UNIT(10, 12, 2, 0, 18, 7, 5, [OpressorCannon, CoaxialAutoCannon, MultiMelta, MultiMelta, MeltaGun, MeltaGun, HeavyStubber, PulziverCannon])
    
    # settings
    range_ = 18
    N = 100000
    
    d1 = RogalDornBattleTank.get_data_damage_target(LemanRussDemolisher, range_, N)
    d2 = LemanRussDemolisher.get_data_damage_target(RogalDornBattleTank, range_, N)
    
    RD_pc = RogalDornBattleTank.get_success_percent_damage_on_target(LemanRussDemolisher, d1)
    LR_pc = LemanRussDemolisher.get_success_percent_damage_on_target(RogalDornBattleTank, d2)
     
    violinplots([d1, d2], plt.gca(), ['Dorn {:.2f}'.format(RD_pc), 'Russ {:.2f}'.format(LR_pc)])
    plt.title('Lethal')
    plt.show()
        
