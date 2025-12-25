#!/usr/bin/env python
# coding: utf-8

import numpy as np
from enum import Enum, auto
import ac_regular
#from frozendict import frozendict

AC_MOVE = Enum('MOVE', ['NORMAL', 'REMAIN_STATIONARY', 'FOLL_BACK', 'ADVANCE'])

class AC_WEAPON(object):        
    
    # TODO move to AC_ABILITIES class
    RAPID_FIRE = 'RAPID_FIRE'
    TORRENT = 'TORRENT'
    MELTA = 'MELTA'
    LETHAL_HITS = 'LETHAL_HITS'
    REROLL_TO_HIT = 'REROLL_TO_HIT'
    REROLL_TO_WOUND = 'REROLL_TO_WOUND'
    DEVASTATING_WOUNDS = 'DEVASTATING_WOUNDS'
    MOVEMENT_TYPE = 'MOVEMENT_TYPE'
    SUSTANED_HITS = 'SUSTANED_HITS'
    IGNORES_COVER = 'IGNORES_COVER'
    PLUS_BS = 'PLUS_BS'
    IN_COVER = 'IN_COVER'
    IGNORE_DAMAGE = 'IGNORE_DAMAGE'
    PLUS_AP = 'PLUS_AP'
    # guard
    FRFSRF = 'FRFSRF'
    PLUS_STR = 'PLUS_STR'
    
    '''
    Constructs weapon class
    args:
        range_ - max range of weapon 
        attacks - number of attacks, can be like 3d3+2
        skill - ballistic or weapon skill, int
        strength - 
        ap - 
        damage - damage, can be like 2d6
        *args - abilities without parameters, like TORRENT, ASSAULT, HEAVY etc.
        **kwargs - abilities with paameters, like RAPID_FIRE 1, SUSTANED_HITS 2 etc.
    '''
    def __init__(self, range_, attacks, skill, strength, ap, damage, name, *args, **kwargs):
        
        self.args_abilities = args
        self.kwargs_abilities = kwargs
        
        self.name = name
        if isinstance(attacks, int):
            self.attacks = attacks
        elif isinstance(attacks, str):
            self.attacks = ac_regular.AC_REGULAR(attacks)
        else:
            raise TypeError('AC_WEAPON.__init__: attacks must be an integer or string')                
        if not isinstance(range_, int):
            raise TypeError('AC_WEAPON.__init__: range_ must be an integer')
        self.range = range_
        if not isinstance(strength, int):
            raise TypeError('AC_WEAPON.__init__: strength must be an integer')
        self.strength = strength
        if not isinstance(ap, int):
            raise TypeError('AC_WEAPON.__init__: ap must be an integer')
        self.ap = np.abs(ap) # if some one put -2        
        
        if isinstance(damage, int):
            self.damage = damage
        elif isinstance(damage, str):
            self.damage = ac_regular.AC_REGULAR(damage)
        else:
            raise TypeError('AC_WEAPON.__init__: damage must be an integer or string')
        
        if isinstance(skill, int):
            self.skill = skill
        else:
            raise TypeError('AC_WEAPON.__init__: skill must be integer')
        
        self.critical_hit = 6
        self.critical_wound = 6
        #print(args)
                
        
    #def __eq__(self, other):
        #if not isinstance(other, AC_WEAPON):
            #return NotImplemented
        ##if self.name == 'Meltagun':# and other.name == 'Meltagun':
            ##print(self.__dict__)
            ##print(other.__dict__)
            ##print('/n')
        #return self.__dict__ == other.__dict__        
    
    #def __hash__(self):
        #def to_hashable(obj):
            #if isinstance(obj, dict):
                #return frozenset((k, to_hashable(v)) for k, v in obj.items())
            #elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
                #return frozenset(to_hashable(item) for item in obj)
            #return obj  # primitives are hashable
    
        #hashable_items = ((k, to_hashable(v)) for k, v in self.__dict__.items() 
                      #if not k.startswith('_'))
        #return hash(frozenset(hashable_items))
     
            
    def _attacks(self):
        if isinstance(self.attacks, int):
            return self.attacks
        else:
            return self.attacks.roll()
    
    
    def _damage(self):
        if isinstance(self.damage, int):
            return self.damage
        else:
            return self.damage.roll()
    
    '''
    Gives number of attacks from weapon
    args:
        range_ - distance to target
    '''
    def get_attacks(self, range_ = 0):
        if range_ > self.range:
            return 0
        attacks = 0
        if AC_WEAPON.RAPID_FIRE in self.kwargs_abilities and range_ <= self.range /2 :            
            attacks += self._attacks()+self.kwargs_abilities[AC_WEAPON.RAPID_FIRE]            
        else:
            attacks += self._attacks()
        if AC_WEAPON.RAPID_FIRE in self.kwargs_abilities and AC_WEAPON.FRFSRF in self.args_abilities:
            attacks += 1
        return attacks
            
        
    '''
    Gives number of hits
    args:
        range_ - distance to target
    returns:
        hits - 
        wounds - if LETHAL_HITS are here
    '''
    def get_hits(self, range_ = 0):
        attacks = self.get_attacks(range_)
        
        hits = 0
        wounds = 0
        value_to_hit = self.skill
        # TODO modifiers
        if AC_WEAPON.PLUS_BS in self.args_abilities:
            value_to_hit = max(2, value_to_hit - 1)
        
        if AC_WEAPON.TORRENT in self.args_abilities:
            return attacks, 0
        
        for i in range(attacks):
            die = ac_regular.roll_d6()
            # rr here
            if AC_WEAPON.REROLL_TO_HIT in self.args_abilities:
                if die < value_to_hit:
                    die = ac_regular.roll_d6()
                    
            if AC_WEAPON.REROLL_TO_HIT in self.kwargs_abilities:
                if die < value_to_hit and die <= self.kwargs_abilities[AC_WEAPON.REROLL_TO_HIT]:
                    die = ac_regular.roll_d6()        
            
            if( die != 1):
                
                if die >= self.critical_hit:
                    if AC_WEAPON.LETHAL_HITS in self.args_abilities:
                        wounds += 1
                    else:
                        hits += 1
                    if AC_WEAPON.SUSTANED_HITS in self.kwargs_abilities:
                        hits += self.kwargs_abilities[AC_WEAPON.SUSTANED_HITS]
                elif die >= value_to_hit:
                    hits += 1
        return hits, wounds

    '''
    get wounds
    '''
    def get_wounds(self, target, range_ = 0):
        hits, wounds = self.get_hits(range_)
        
        saves, no_saves = wounds, 0
        
        strength = self.strength
        if AC_WEAPON.PLUS_STR in self.args_abilities:
            strength += 1
        
        if strength *2 <= target.toughness:
            to_wound_value = 6
        elif strength < target.toughness:
            to_wound_value = 5
        elif strength == target.toughness:
            to_wound_value = 4
        elif strength >= target.toughness * 2:
            to_wound_value = 2
        else:
            to_wound_value = 3
        
        # TODO modifiers
        
        for i in range(hits):
            
            die = ac_regular.roll_d6()
            # full
            if AC_WEAPON.REROLL_TO_WOUND in self.args_abilities:
                if die < to_wound_value:
                    die = ac_regular.roll_d6()
                    
            elif AC_WEAPON.REROLL_TO_WOUND in self.kwargs_abilities:
                if die < to_wound_value and die <= self.kwargs_abilities[AC_WEAPON.REROLL_TO_WOUND]:
                    die = ac_regular.roll_d6()        
                    
            # TODO RR
            if die != 1:
                if die >= self.critical_wound:
                    if AC_WEAPON.DEVASTATING_WOUNDS in self.args_abilities:
                        no_saves += 1
                    else:
                        saves += 1
                elif die >= to_wound_value:
                    saves += 1
        
        #print(saves)
        return saves, no_saves
    
    def get_damage(self, target, range_ = 0):
        
        ap = self.ap
        if AC_WEAPON.PLUS_AP in self.args_abilities:
            ap += 1
        
        damage = 0
        saves, no_saves = self.get_wounds(target, range_)
        damages = no_saves
        save = target.save + ap 
        
        if AC_WEAPON.IN_COVER in target.args_abilities and not (AC_WEAPON.IGNORES_COVER in self.args_abilities):
            if save != 3 and ap != 0:
                save = max(2, save-1)
        
        if target.invul != 0:
            save = min(save, target.invul)
        
        for i in range(saves):
            die = ac_regular.roll_d6()
            
            if die == 1 or die < save:
                damages += 1
                
        for i in range(damages):   
            damage += self._damage()
            if AC_WEAPON.MELTA in self.kwargs_abilities and range_ <= self.range/2:
                damage += self.kwargs_abilities[AC_WEAPON.MELTA]
        
        #TODO FNP
        
        return damage
        
        
    def get_damage_models(self, target, range_ = 0):
        
        ap = self.ap
        if AC_WEAPON.PLUS_AP in self.args_abilities:
            ap += 1
        
        
        saves, no_saves = self.get_wounds(target, range_)        
        save = target.save + ap 
        
        unsuccessfull_saves = 0
        
        if AC_WEAPON.IN_COVER in target.args_abilities and not (AC_WEAPON.IGNORES_COVER in self.args_abilities):
            if not (target.save == 3 and ap == 0):
                save = max(2, save-1)
        
        if target.invul != 0:
            save = min(save, target.invul)
        
        for i in range(saves):
            die = ac_regular.roll_d6()
            
            if die == 1 or die < save:
                unsuccessfull_saves += 1
        
        models_killed = 0
        damage = 0
        for i in range(unsuccessfull_saves + no_saves):   
            damage += self._damage()
            if AC_WEAPON.MELTA in self.kwargs_abilities and range_ <= self.range/2:
                damage += self.kwargs_abilities[AC_WEAPON.MELTA]
            if damage >= target.wounds:
                models_killed += 1
                damage = 0
        
        models_killed += damage / target.wounds
        
        #TODO FNP
        
        return models_killed
            
if __name__ == '__main__' :
    
    args = [AC_WEAPON.FRFSRF]
    print(args)
    lasgun = AC_WEAPON(24, 1, 4, 3, 0, 1, "lasgun", *args, RAPID_FIRE = 1)        
    
    print(lasgun.get_attacks(9.1))
    #print(lasgun.get_hits())
    
    
    #flamer = AC_WEAPON(12, 'd6', 0, 4, 0, 1, AC_WEAPON.TORRENT)
    ##print(flamer.get_attacks(1))
    #print(flamer.get_hits())
