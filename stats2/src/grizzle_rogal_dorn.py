#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import ac_squad
from ac_plot import violinplots, plot_series
import matplotlib.pyplot as plt


if __name__ == '__main__':
    
    NO_NO_NO_MELTA = 21
    NO_NO_MELTA = 17
    NO_MELTA = 10
    M_MELTA = 8
    F_MELTA = 5
    N = 10000
    
    #RANGE = NO_NO_NO_MELTA
    #RANGE = F_MELTA
    

    
    test_scenarious = {}
    
    test_scenarious['T_AIM'] = ([ac_weapon.AC_WEAPON.PLUS_BS], 
                                {'REROLL_TO_HIT': 1})
    
    test_scenarious['+AP'] = ([ac_weapon.AC_WEAPON.PLUS_AP], 
                                {'REROLL_TO_HIT': 1})
    
    test_scenarious['T_AIM_RR2W1'] = ([ac_weapon.AC_WEAPON.PLUS_BS], 
                                {'REROLL_TO_HIT': 1, 'REROLL_TO_WOUND': 1})
    
    test_scenarious['+AP_RR2W1'] = ([ac_weapon.AC_WEAPON.PLUS_AP], 
                                {'REROLL_TO_HIT': 1, 'REROLL_TO_WOUND': 1})
    
    test_scenarious['T_AIM_RR2W1_LETHALS'] = ([ac_weapon.AC_WEAPON.PLUS_BS, ac_weapon.AC_WEAPON.LETHAL_HITS], 
                                {'REROLL_TO_HIT': 1, 'REROLL_TO_WOUND': 1})
    
    test_scenarious['+AP_RR2W1_LETHALS'] = ([ac_weapon.AC_WEAPON.PLUS_AP, ac_weapon.AC_WEAPON.LETHAL_HITS], 
                                {'REROLL_TO_HIT': 1, 'REROLL_TO_WOUND': 1})
    
    
    for RANGE in [F_MELTA, M_MELTA, NO_MELTA, NO_NO_MELTA, NO_NO_NO_MELTA]:
        LABELS = []
        DATA = []
        
        
        title = f"RogalDorn on dist={RANGE}\" against different targets"
        for name, (abilities, kwabilities) in test_scenarious.items():
            LABELS.append(name)
        
            # weapons    
            MultiMelta = ac_weapon.AC_WEAPON(18, 2, 4, 9, 4, 'd6', 'MultiMelta', MELTA = 2)
            HeavyStubber = ac_weapon.AC_WEAPON(36, 3, 4, 4, 0, 1, 'HeavyStubber', RAPID_FIRE = 3)    
            
            OpressorCannon = ac_weapon.AC_WEAPON(60, 'd6+3', 4, 12, 2, 3, 'OpressorCannon')
            CoaxialAutoCannon = ac_weapon.AC_WEAPON(48, 2, 4, 9, 1, 3, 'CoaxialAutoCannon')
            PulziverCannon = ac_weapon.AC_WEAPON(24, 'd6', 4, 9, 3, 3, 'PulziverCannon')
            MeltaGun = ac_weapon.AC_WEAPON(12, 1, 4, 9, 4, 'd6', 'MeltaGun', MELTA = 2)
            
            # units    
            Dorn = ac_unit.AC_UNIT(10, 12, 2, 0, 18, 7, 5, 
                                        [OpressorCannon, 
                                        CoaxialAutoCannon, 
                                        PulziverCannon,
                                        MultiMelta, 
                                        MultiMelta, 
                                        MeltaGun, 
                                        MeltaGun, 
                                        HeavyStubber,                                     
                                        ], 
                                        *abilities,
                                        **kwabilities
                                        )
                                        
            RogalDorn = ac_squad.AC_SQUAD([(Dorn, 1)])
                                        
            targets = [ac_unit.AC_UNIT(6, 4, 3, 0, 2, 6, 2, []),
                    ac_unit.AC_UNIT(6, 4, 3, 0, 2, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER), 
                    ac_unit.AC_UNIT(6, 6, 3, 0, 2, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER),
                    ac_unit.AC_UNIT(5, 5, 2, 4, 3, 6, 2, []),
                    ac_unit.AC_UNIT(5, 5, 2, 4, 3, 6, 2, [], ac_weapon.AC_WEAPON.IN_COVER),                   
                    ac_unit.AC_UNIT(6, 10, 3, 0, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER),
                    ac_unit.AC_UNIT(6, 11, 2, 0, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER),
                    ac_unit.AC_UNIT(6, 11, 2, 4, 11, 6, 3, [], ac_weapon.AC_WEAPON.IN_COVER)
                    ]
            
            d = []
            for target in targets:
                d.append(RogalDorn._get_data_damage_single_target_with_wounds(target, RANGE, N))
            DATA.append(d)
            print(f"Done with {name}")
            
        plot_series( DATA, plt.gca(), LABELS,  ['on SM', 'on SM cover', 'on plague cover', 'on termi', 'on termi cover', 'tank t10 3+', 'tank t11 2+', 'tank t11 2+ 4++'], between = False)
        plt.grid()
        plt.ylabel("Models killed")
        plt.title(title)
        
        plt.show()
