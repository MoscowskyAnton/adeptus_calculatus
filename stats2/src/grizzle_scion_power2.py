#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import ac_squad
from ac_plot import violinplots, plot_series
import matplotlib.pyplot as plt



if __name__ == '__main__':
         
    title = f"Different scion-bombs on different targets"        
    
    
    base_stats = [6, 3, 4, 0, 1, 7, 1]
    
    abilities = [ac_weapon.AC_WEAPON.FRFSRF, ac_weapon.AC_WEAPON.PLUS_BS]
    kwabilities = {'SUSTANED_HITS': 1, 'REROLL_TO_WOUND': 1, 'REROLL_TO_HIT': 1}

    HotShotLasgun = ac_weapon.AC_WEAPON(24, 1, 3, 3, 1, 1, "HotShotLasgun", RAPID_FIRE = 1)
    HotShotVolleyGun = ac_weapon.AC_WEAPON(30, 2, 3, 4, 1, 1, "HotShotVolleyGun", RAPID_FIRE = 2)
    HotShotLaspistol = ac_weapon.AC_WEAPON(12, 1, 3, 3, 1, 1, "HotShotLaspistol")
    PlasmaGun = ac_weapon.AC_WEAPON(24, 1, 3, 8, 3, 2, "PlasmaGun", RAPID_FIRE = 1)
    PlasmaPistol = ac_weapon.AC_WEAPON(12, 1, 3, 8, 3, 2, "PlasmaPistol")
    Meltagun = ac_weapon.AC_WEAPON(12, 1, 3, 9, 4, 'd6', "Meltagun", MELTA = 2)
    Grenade = ac_weapon.AC_WEAPON(24, 1, 3, 9, 2, 'd3', "GrenadeLauncher")
        
    TempestorPrime = ac_unit.AC_UNIT(*base_stats, [], *abilities, **kwabilities)
    Tempestor = ac_unit.AC_UNIT(*base_stats, [PlasmaPistol], *abilities, **kwabilities)
    PlasmaGunner = ac_unit.AC_UNIT(*base_stats, [PlasmaGun], *abilities, **kwabilities)
    MeltaGunner = ac_unit.AC_UNIT(*base_stats, [Meltagun], *abilities, **kwabilities)
    Lasgunner = ac_unit.AC_UNIT(*base_stats, [HotShotLasgun], *abilities, **kwabilities)
    Voxer = ac_unit.AC_UNIT(*base_stats, [HotShotLaspistol], *abilities, **kwabilities)
    Volley = ac_unit.AC_UNIT(*base_stats, [HotShotVolleyGun], *abilities, **kwabilities)
    Medic = ac_unit.AC_UNIT(*base_stats, [HotShotLaspistol, HotShotLasgun], *abilities, **kwabilities)
    Grenadier = ac_unit.AC_UNIT(*base_stats, [Grenade], *abilities, **kwabilities)

    
    SQUADS = {}
    
    SQUADS['BigMeltaSquad'] = ac_squad.AC_SQUAD([(TempestorPrime, 1),
                                                 (Tempestor, 1),
                                                 (Voxer, 1),
                                                 (Grenadier, 1),
                                                 (PlasmaGunner, 3),                                
                                                 (MeltaGunner, 3),
                                                 (Lasgunner, 4),
                                                 (Medic, 1)
                                                 ])
    
    SQUADS['BigVolleySquad'] = ac_squad.AC_SQUAD([(TempestorPrime, 1),
                                                  (Tempestor, 1),
                                                  (Voxer, 1),
                                                  (MeltaGunner, 1),
                                                  (PlasmaGunner, 3),
                                                  (Volley, 3),                                
                                                  (Lasgunner, 4),
                                                  (Medic, 1)
                                                  ])
    
    SQUADS['SmallMeltaSquad'] = ac_squad.AC_SQUAD([(TempestorPrime, 1),
                                                 (Tempestor, 1),
                                                 (Voxer, 1),
                                                 (Grenadier, 1),
                                                 (PlasmaGunner, 2),                                
                                                 (MeltaGunner, 2),
                                                 (Lasgunner, 1),
                                                 (Medic, 1)
                                                 ])
    
    LABELS = []
    DATA = []
                
        
    for name, squad in SQUADS.items():
        LABELS.append(name)
                            
        targets = [ac_unit.AC_UNIT(6, 3, 4, 0, 1, 6, 1, []),
                   ac_unit.AC_UNIT(6, 3, 4, 0, 1, 6, 1, [], ac_weapon.AC_WEAPON.IN_COVER),
                   ac_unit.AC_UNIT(6, 4, 3, 0, 2, 6, 2, []),
                   ac_unit.AC_UNIT(6, 4, 3, 0, 2, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER), 
                   ac_unit.AC_UNIT(6, 6, 3, 0, 2, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER),
                   ac_unit.AC_UNIT(5, 5, 2, 4, 3, 6, 2, []),
                   ac_unit.AC_UNIT(5, 5, 2, 4, 3, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER),                   
                   ac_unit.AC_UNIT(6, 10, 3, 0, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER),                   
                   ]
        
        N = 10000
        
        d = []
        for target in targets:
            d.append(squad._get_data_damage_single_target_with_wounds(target, 9.1, N))
        DATA.append(d)
                        
        print(f"Done with {name}")
    
    plot_series( DATA, plt.gca(), LABELS,  ['T3 4+', 'T3 4+ cover', 'SM', 'SM cover', 'plague cover', 'termi', 'termi cover', 'tank t10 3+ cover'], between = False, add_cmp_text_on_data = 2)
    plt.grid()
    plt.ylabel("Models killed")
    plt.title(title)

    plt.show()
    
