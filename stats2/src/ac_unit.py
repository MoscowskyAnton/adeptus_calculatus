#!/usr/bin/env python
# coding: utf-8
import ac_weapon
from enum import Enum, auto

class AC_UNIT_TYPE(Enum):
    INFATRY = auto()
    VEHICLE = auto()
    CAVALERY = auto()
    OTHER = auto()

class AC_SHOOT_ATACKER(object):

    def __init__(self, bs, **abilities):
        self.bs = bs
        
        self.abilities = abilities
        
        self.weapons = []

    '''
    Registes a weapon for model
    '''
    def give_weapon(self, weapon):
        if not isinstance(weapon, ac_weapon.AC_WEAPON):
            raise ValueError("Weapon must be AC_WEAPON")
        
        self.weapons.append(weapon)
        

class AC_DEFENDER(object):
    
    def __init__(self, toughness, armour, invul = None, **abilities):        
        self.toughness = toughness
        self.armour = armour
        self.invul = invul
        
        self.abilities = abilities
        
