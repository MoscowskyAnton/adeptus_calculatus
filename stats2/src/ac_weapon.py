#!/usr/bin/env python
# coding: utf-8

import numpy as np
from enum import Enum, auto
from ac_regular import AC_REGULAR
        

class AC_WEAPON_TYPE(Enum):
    HEAVY = auto()
    ASSAULT = auto()
    RAPID_FIRE = auto()
    PISTOL = auto()
    MELEE = auto()
    OTHER = auto()
    
    def __str__(self):
        return self.name

class AC_WEAPON(object):        
    
    def __init__(self, type_, shots, range_, strength, ap, **abilities):
        if not isinstance(type_, AC_WEAPON_TYPE):
            raise TypeError('AC_WEAPON.__init__: type_ must be an AC_WEAPON_TYPE')
        self.type = type_
        if isinstance(shots, int):
            self.shots = shots
        elif isinstance(shots, str):
            self.shots = AC_REGULAR(shots)
        else:
            raise TypeError('AC_WEAPON.__init__: shots must be an integer or tring')                
        if not isinstance(range_, int):
            raise TypeError('AC_WEAPON.__init__: range_ must be an integer')
        self.range = range_
        if not isinstance(strength, int):
            raise TypeError('AC_WEAPON.__init__: strength must be an integer')
        self.strength = strength
        if not isinstance(ap, int):
            raise TypeError('AC_WEAPON.__init__: ap must be an integer')
        self.ap = np.abs(ap)
        
        self.abilities = abilities
            
    '''
    Gives number of shots from weapon
    args:
        range_ 
    '''
    def get_shots(self, range_ = 0):
        if range_ > self.range:
            return 0
        if self.type != AC_WEAPON_TYPE.RAPID_FIRE or range_ > self.range /2 :            
            if isinstance(self.shots, int):
                return self.shots
            else:
                return self.shots.roll()
        else:
            if isinstance(self.shots, int):
                return self.shots*2
            else:
                return self.shots.roll()*2 # ???
        


if __name__ == '__main__' :
    
    hot_shot_lasgun = AC_WEAPON(AC_WEAPON_TYPE.RAPID_FIRE, 1, 24, 3, 2)
    print(hot_shot_lasgun.get_shots(11))
    
    flamer = AC_WEAPON(AC_WEAPON_TYPE.ASSAULT, 'd6', 12, 3, 0)
    print(flamer.get_shots(13))
