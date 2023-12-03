#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import ac_plot
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    LasCannon = ac_weapon.AC_WEAPON(48, 1, 4, 12, 3, 'd6+1')
    MultiMelta = ac_weapon.AC_WEAPON(18, 2, 4, 9, 4, 'd6', MELTA = 2)
    HeavyStubber = ac_weapon.AC_WEAPON(36, 3, 4, 4, 0, 1, RAPID_FIRE = 3)
    DemolisherCannon = ac_weapon.AC_WEAPON(24, 'd6+3', 4, 14, 3, 'd6')
    HunterKillerMissile = ac_weapon.AC_WEAPON(48, 1, 4, 14, 3, 'd6')
    
    
    LemanRussDemolisherLH = ac_unit.AC_UNIT(10, 11, 2, 0, 13, 7, 3, 
                                  [DemolisherCannon, 
                                   LasCannon, 
                                   MultiMelta, 
                                   MultiMelta, 
                                   HeavyStubber, 
                                   #HunterKillerMissile
                                   ], 
                                  ac_weapon.AC_WEAPON.LETHAL_HITS, 
                                  ac_weapon.AC_WEAPON.PLUS_BS
                                  #ac_weapon.AC_WEAPON.IN_COVER
                                  )
    
    LemanRussDemolisher = ac_unit.AC_UNIT(10, 11, 2, 0, 13, 7, 3, 
                                  [DemolisherCannon, 
                                   LasCannon, 
                                   MultiMelta, 
                                   MultiMelta, 
                                   HeavyStubber, 
                                   #HunterKillerMissile
                                   ], 
                                  #ac_weapon.AC_WEAPON.LETHAL_HITS, 
                                  ac_weapon.AC_WEAPON.PLUS_BS
                                  #ac_weapon.AC_WEAPON.IN_COVER
                                  )
    
    
    GladiatorLancer = ac_unit.AC_UNIT(10, 10, 3, 0, 12, 6, 3, [],
                                      ac_weapon.AC_WEAPON.IN_COVER)
    
    
    N = 100000
    
    data_stationary_melta = LemanRussDemolisherLH.get_data_damage_target(GladiatorLancer, 10, N)
    data_stationary_no_melta = LemanRussDemolisherLH.get_data_damage_target(GladiatorLancer, 20, N)
    data_full_melta = LemanRussDemolisher.get_data_damage_target(GladiatorLancer, 8, N)
    data_melta = LemanRussDemolisher.get_data_damage_target(GladiatorLancer, 10, N)
    
    stat_melta_pc = LemanRussDemolisherLH.get_success_percent_damage_on_target(GladiatorLancer, data_stationary_melta)
    stat_no_melta_pc = LemanRussDemolisherLH.get_success_percent_damage_on_target(GladiatorLancer, data_stationary_no_melta)
    melta_pc = LemanRussDemolisher.get_success_percent_damage_on_target(GladiatorLancer, data_full_melta)
    melta_small_pc = LemanRussDemolisher.get_success_percent_damage_on_target(GladiatorLancer, data_melta) 
    
    ac_plot.violinplots([data_stationary_melta, 
                         data_full_melta, 
                         data_melta,
                         data_stationary_no_melta                         
                         ], plt.gca(), ['LH small melta {:.2f}'.format(stat_melta_pc), 
                                        'Full Melta (no LH) {:.2f}'.format(melta_pc), 
                                        'Small Melta (no LH) {:.2f}'.format(melta_small_pc),
                                        'LH no melta {:.2f}'.format(stat_no_melta_pc)]
                                        )
    plt.title('Lethal vs melta on LRD')
    plt.show()
    
