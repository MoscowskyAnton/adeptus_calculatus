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
        
        
        
        
    def attack_target(self, target, range_):
        
        pass
    
    def _attack_single_target(self, target_unit, range_):
        total_damage = 0
        for unit in self.units:
            total_damage += unit.attack_target(target_unit, range_)
        
        return total_damage
    
    def _get_data_damage_single_target(self, target, range_, N):
        data = []
        for i in range(N):
            data.append(self._attack_single_target(target, range_))
        return data
    
    
if __name__ == '__main__':
    
    '''
    HotShotLasCarabin = ac_weapon.AC_WEAPON(18, 2, 3, 3, 1, 1)
    
    TempestusAquilonBlank = ac_unit.AC_UNIT(6, 3, 3, 0, 1, 7, 1, [])
    
    TempestusAquilonWithHotShotLasCarabin = copy.copy(TempestusAquilonBlank)
    TempestusAquilonWithHotShotLasCarabin.add_weapons([HotShotLasCarabin])
    
    
    TempestusAquilons = AC_SQUAD([(TempestusAquilonWithHotShotLasCarabin, 8),
                                ])
    '''
    
    HotShotLasgun = ac_weapon.AC_WEAPON(24, 1, 3, 3, 1, 1, RAPID_FIRE = 1)
    HotShotVolleyGun = ac_weapon.AC_WEAPON(30, 2, 3, 4, 1, 1, RAPID_FIRE = 2)
    HotShotLaspistol = ac_weapon.AC_WEAPON(12, 1, 3, 3, 1, 1)
    PlasmaGun = ac_weapon.AC_WEAPON(24, 1, 3, 8, 3, 2, RAPID_FIRE = 1)
    PlasmaPistol = ac_weapon.AC_WEAPON(12, 1, 3, 8, 3, 2)
    Meltagun = ac_weapon.AC_WEAPON(12, 1, 3, 9, 4, 'd6', MELTA = 2)
    
    
    base_stats = [6, 3, 4, 0, 1, 7, 1]
    abilities = [ac_weapon.AC_WEAPON.FRFSRF]
    kwabilities = {'SUSTANED_HITS': 2, 'REROLL_TO_WOUND': 1}
    TempestorPrime = ac_unit.AC_UNIT(*base_stats, [], *abilities, **kwabilities)
    Tempestor = ac_unit.AC_UNIT(*base_stats, [PlasmaPistol], *abilities, **kwabilities)
    PlasmaGunner = ac_unit.AC_UNIT(*base_stats, [PlasmaGun], *abilities, **kwabilities)
    MeltaGunner = ac_unit.AC_UNIT(*base_stats, [Meltagun], *abilities, **kwabilities)
    Lasgunner = ac_unit.AC_UNIT(*base_stats, [HotShotLasgun], *abilities, **kwabilities)
    Voxer = ac_unit.AC_UNIT(*base_stats, [PlasmaPistol], *abilities, **kwabilities)
    Volley = ac_unit.AC_UNIT(*base_stats, [HotShotVolleyGun], *abilities, **kwabilities)
    
    BigScionSquad = AC_SQUAD([(TempestorPrime, 1),
                          (Tempestor, 1),
                          (Voxer, 1),
                          (Volley, 1),
                          (PlasmaGunner, 3),
                          (MeltaGunner, 3),
                          (Lasgunner, 5)
                          ])
    
    SpaceMarine = ac_unit.AC_UNIT(6, 4, 3, 0, 2, 6, 2)
    Terminator = ac_unit.AC_UNIT(5, 5, 3, 4, 2, 6, 3)
    
    N = 10000
    
    twsm = BigScionSquad._get_data_damage_single_target(SpaceMarine, 9.1, N)
    twt = BigScionSquad._get_data_damage_single_target(Terminator, 9.1, N)
    #print(twsm, twt)
    violinplots( [twsm, twt], plt.gca(), ['on SM', 'on termi'], add_text = True)
    plt.show()
    
    
