#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import copy

class AC_SQUAD(object):
    
    
    def __init__(self, units = [], *args, **kwargs):
        
        # TODO: check values
        self.units = units
        
        
    def attack_target(self, target, range_):
        
        pass
    
    
if __name__ == '__main__':
    
    
    HotShotLasCarabin = ac_weapon.AC_WEAPON(18, 2, 3, 3, 1, 1)
    
    TempestusAquilonBlank = ac_unit.AC_UNIT(6, 3, 3, 0, 1, 7, 1, [])
    
    TempestusAquilonWithHotShotLasCarabin = copy.copy(TempestusAquilonBlank)
    TempestusAquilonWithHotShotLasCarabin.add_weapons([HotShotLasCarabin])
    
    
    TempestusAquilons = AC_SQUAD([(TempestusAquilonWithHotShotLasCarabin, 8),
                                  ])
