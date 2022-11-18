#!/usr/bin/env python
# coding: utf-8

import numpy as np
from enum import Enum, auto

        
        

class AC_WEAPON_TYPE(Enum):
    HEAVY = auto()
    ASSAULT = auto()
    RAPID_FIRE = auto()
    PISTOL = auto()
    MELEE = auto()
    
    def __str__(self):
        return self.name

class AC_WEAPON(object):        
    
    def __init__(self, type_, shots, range_, strength, ap, **abilities):
        if not isinstance(type_, AC_WEAPON_TYPE):
            raise TypeError('AC_WEAPON.__init__: type_ must be an AC_WEAPON_TYPE')
        self.type = type_
        if not (isinstance(shots, int) or isinstance(shots, AC_RANDOM)):
            raise TypeError('AC_WEAPON.__init__: shots must be an integer')
        self.shots = shots
        if not isinstance(range_, int):
            raise TypeError('AC_WEAPON.__init__: range_ must be an integer')
        self.range = range_
        if not isinstance(strength, int):
            raise TypeError('AC_WEAPON.__init__: strength must be an integer')
        self.strength = strength
        if not isinstance(ap, int):
            raise TypeError('AC_WEAPON.__init__: ap must be an integer')
        self.ap = np.abs(ap)
            
    def get_shots(self, range_):
        if range_ > self.range:
            return 0
        


if __name__ == '__main__' :
