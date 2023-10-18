#!/usr/bin/env python
# coding: utf-8
import ac_weapon
from enum import Enum, auto
import copy
import matplotlib.pyplot as plt

class AC_UNIT(object):
    
    IN_COVER = 'IN_COVER'
    
    def __init__(self, movement, toughness, save, invul, wounds, leadership, oc, weapons = [], *args, **kwargs):
            
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.invul = invul
        self.wounds = wounds
        self.leadership = leadership
        self.oc = oc
        
        self.weapons = []
        for wep in weapons:
            self.weapons.append(copy.copy(wep))
        
        self.args_abilities = args
        self.kwargs_abilities = kwargs
    
    
    def attack_target(self, target, range_):
        
        total_damage = 0
        for weapon in self.weapons:
            total_damage += weapon.get_damage(target, range_)
            
        return total_damage
            
    
    def mean_damage_target(self, target, range_, N):
        td = 0
        for i in range(N):
            td += self.attack_target(target, range_)
        return td / N
    
    def set_data_damage_target(self, target, range_, N):
        data = []
        for i in range(N):
            data.append(self.attack_target(target, range_))
        return data
        
    
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
    
    # units
    LemanRussDemolisher = AC_UNIT(10, 11, 2, 0, 13, 7, 3, [DemolisherCannon, LasCannon, MultiMelta, MultiMelta, HeavyStubber, HunterKillerMissile])
    
    RogalDornBattleTank = AC_UNIT(10, 12, 2, 0, 18, 7, 5, [OpressorCannon, CoaxialAutoCannon, MultiMelta, MultiMelta, HeavyStubber, HeavyStubber, HeavyStubber, PulziverCannon])
    
    range_ = 18
    N = 1000
    
    #print(f'Damage of RogalDorn on LemanRussDemolisher at {range_}\" is {RogalDornBattleTank.mean_damage_target(LemanRussDemolisher, range_, N)}')
    
    #print(f'Damage of LemanRussDemolisher on RogalDorn at {range_}\" is {LemanRussDemolisher.mean_damage_target(RogalDornBattleTank, range_, N)}')


    
    d1 = RogalDornBattleTank.set_data_damage_target(LemanRussDemolisher, range_, N)
    d2 = LemanRussDemolisher.set_data_damage_target(RogalDornBattleTank, range_, N)
    
    plt.violinplot([d1, d2], showmeans = True, showextrema = False)
    plt.show()
        
