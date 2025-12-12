#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import ac_squad
from ac_plot import violinplots, plot_series
import matplotlib.pyplot as plt



if __name__ == '__main__':
    
    
    test_scenarious = {}
    test_scenarious['FRFSRF'] = ([ac_weapon.AC_WEAPON.FRFSRF], 
                                 {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1})
    
    test_scenarious['T_AIM'] = ([ac_weapon.AC_WEAPON.PLUS_BS], 
                                 {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1})
    
    test_scenarious['RR1+FRFSRF+T_AIM'] = ([ac_weapon.AC_WEAPON.FRFSRF, ac_weapon.AC_WEAPON.PLUS_BS], 
                                           {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1, 'REROLL_TO_HIT': 1})
    
    test_scenarious['RR1+FRFSRF+AP'] = ([ac_weapon.AC_WEAPON.FRFSRF, ac_weapon.AC_WEAPON.PLUS_AP], 
                                        {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1, 'REROLL_TO_HIT': 1})
    
    '''
    test_scenarious['FRFSRF+AP'] = ([ac_weapon.AC_WEAPON.FRFSRF, ac_weapon.AC_WEAPON.PLUS_AP], 
                                    {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1})
    '''
    test_scenarious['RR1+T_AIM+AP'] = ([ac_weapon.AC_WEAPON.PLUS_BS, ac_weapon.AC_WEAPON.PLUS_AP], 
                                       {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1, 'REROLL_TO_HIT': 1})
    
    LABELS = []
    DATA = []
    
    HotShotLasgun = ac_weapon.AC_WEAPON(24, 1, 3, 3, 1, 1, name = "HotShotLasgun", RAPID_FIRE = 1)
    HotShotVolleyGun = ac_weapon.AC_WEAPON(30, 2, 3, 4, 1, 1, name = "HotShotVolleyGun", RAPID_FIRE = 2)
    HotShotLaspistol = ac_weapon.AC_WEAPON(12, 1, 3, 3, 1, 1, name = "HotShotLaspistol")
    PlasmaGun = ac_weapon.AC_WEAPON(24, 1, 3, 8, 3, 2, name = "PlasmaGun", RAPID_FIRE = 1)
    PlasmaPistol = ac_weapon.AC_WEAPON(12, 1, 3, 8, 3, 2, name = "PlasmaPistol")
    Meltagun = ac_weapon.AC_WEAPON(12, 1, 3, 9, 4, 'd6', name = "Meltagun", MELTA = 2)
    #print(Meltagun.name)    
    base_stats = [6, 3, 4, 0, 1, 7, 1]
    
    
    for name, (abilities, kwabilities) in test_scenarious.items():
        LABELS.append(name)
        
        if name == 'FRFSRF':
            TempestorPrime = ac_unit.AC_UNIT(*base_stats, [PlasmaPistol], *abilities, **kwabilities)
        else:
            TempestorPrime = ac_unit.AC_UNIT(*base_stats, [], *abilities, **kwabilities)
        Tempestor = ac_unit.AC_UNIT(*base_stats, [PlasmaPistol], *abilities, **kwabilities)
        PlasmaGunner = ac_unit.AC_UNIT(*base_stats, [PlasmaGun], *abilities, **kwabilities)
        MeltaGunner = ac_unit.AC_UNIT(*base_stats, [Meltagun], *abilities, **kwabilities)
        Lasgunner = ac_unit.AC_UNIT(*base_stats, [HotShotLasgun], *abilities, **kwabilities)
        Voxer = ac_unit.AC_UNIT(*base_stats, [HotShotLaspistol], *abilities, **kwabilities)
        Volley = ac_unit.AC_UNIT(*base_stats, [HotShotVolleyGun], *abilities, **kwabilities)
        Medic = ac_unit.AC_UNIT(*base_stats, [HotShotLaspistol, HotShotLasgun], *abilities, **kwabilities)
        
        BigScionSquad = ac_squad.AC_SQUAD([(TempestorPrime, 1),
                            (Tempestor, 1),
                            (Voxer, 1),
                            (Volley, 1),
                            (PlasmaGunner, 3),
                            (MeltaGunner, 3),
                            (Lasgunner, 4),
                            (Medic, 1)
                            ])
        
        SpaceMarine = ac_unit.AC_UNIT(6, 4, 3, 0, 2, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER)
        Terminator = ac_unit.AC_UNIT(5, 5, 3, 4, 3, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER)
        PlagueMarine = ac_unit.AC_UNIT(6, 6, 3, 0, 2, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER)
        TankT103p = ac_unit.AC_UNIT(6, 10, 3, 0, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER)
        TankT112p = ac_unit.AC_UNIT(6, 11, 2, 0, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER)
        TankT112p4pp = ac_unit.AC_UNIT(6, 11, 2, 4, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER)
        
        N = 10000
        
        twsm = BigScionSquad._get_data_damage_single_target_with_wounds(SpaceMarine, 9.1, N)
        twpm = BigScionSquad._get_data_damage_single_target_with_wounds(PlagueMarine, 9.1, N)
        twt = BigScionSquad._get_data_damage_single_target_with_wounds(Terminator, 9.1, N)        
        twtank1 = BigScionSquad._get_data_damage_single_target_with_wounds(TankT103p, 9.1, N)
        twtank2 = BigScionSquad._get_data_damage_single_target_with_wounds(TankT112p, 9.1, N)
        twtank3 = BigScionSquad._get_data_damage_single_target_with_wounds(TankT112p4pp, 9.1, N)
        
        DATA.append([twsm, twpm, twt, twtank1, twtank2, twtank3])
        print(f"Done with {name}")
    
    plot_series( DATA, plt.gca(), LABELS,  ['on SM', 'on plague', 'on termi', 'tank t10 3+', 'tank t11 2+', 'tank t11 2+ 4++'], between = False)
    plt.grid()
    plt.xlabel("Models killed")
    plt.title("Scion-bombs on different targets")
    plt.show()
    
