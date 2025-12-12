#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import copy
from ac_plot import violinplots, plot_series
import matplotlib.pyplot as plt


class AC_SQUAD(object):
    
    
    def __init__(self, units = [], *args, **kwargs):
        
        # TODO: check values
        self.units = []
        for (unit, n) in units:
            for _ in range(n):
                self.units.append(copy.deepcopy(unit))
        
        self.args_abilities = args
        self.kwargs_abilities = kwargs
        
        #self.weapon_list = {}
        #for unit in self.units:
            #for weapon in unit.weapons:
                #if weapon in self.weapon_list:
                    #self.weapon_list[weapon] += 1
                #else:
                    #self.weapon_list[weapon] = 1
        #print([(n.name, k) for n, k in self.weapon_list.items()])
        
        self.weapon_list = {}
        for unit in self.units:
            for weapon in unit.weapons:
                if weapon.name == "":
                    print("Warn! Empty weapon name may rion process!")
                if weapon.name in self.weapon_list:
                    self.weapon_list[weapon.name][1] += 1
                else:
                    self.weapon_list[weapon.name] = [weapon, 1]
        
    def attack_target(self, target, range_):        
        pass
    
    def _attack_single_target(self, target_unit, range_):
        total_damage = 0
        #for unit in self.units:
            #total_damage += unit.attack_target(target_unit, range_)
        for weapon_n in self.weapon_list.values():
            weapon = weapon_n[0]
            n = weapon_n[1]
            for _ in range(n):
                total_damage += weapon.get_damage(target_unit, range_)                
        return total_damage
    
    def _get_data_damage_single_target(self, target, range_, N):
        data = []
        for i in range(N):
            data.append(self._attack_single_target(target, range_))
        return data
    
    def _attack_single_target_with_wounds(self, target_unit, range_):
        models_killed = 0
        for weapon_n in self.weapon_list.values():
            weapon = weapon_n[0]
            n = weapon_n[1]
            damage = 0
            for _ in range(n):
                damage += weapon.get_damage(target_unit, range_)                
                if damage >= target_unit.wounds:
                    models_killed += 1
                    damage = 0
        models_killed += (damage/target_unit.wounds)
        return models_killed                        
    
    def _get_data_damage_single_target_with_wounds(self, target, range_, N):
        data = []
        for i in range(N):
            data.append(self._attack_single_target_with_wounds(target, range_))
        return data
    
if __name__ == '__main__':
    
    
    HotShotLasCarabin = ac_weapon.AC_WEAPON(18, 2, 3, 3, 1, 1)
    
    TempestusAquilonBlank = ac_unit.AC_UNIT(6, 3, 3, 0, 1, 7, 1, [])
    
    TempestusAquilonWithHotShotLasCarabin = copy.copy(TempestusAquilonBlank)
    TempestusAquilonWithHotShotLasCarabin.add_weapons([HotShotLasCarabin])
    
    
    TempestusAquilons = AC_SQUAD([(TempestusAquilonWithHotShotLasCarabin, 8),
                                ])
    
    
    
    
