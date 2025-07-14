#!/usr/bin/env python
# coding: utf-8

import ac_unit
import ac_weapon
import ac_plot
import matplotlib.pyplot as plt
from ac_plot import violinplots, plot_series
import numpy as np

if __name__ == '__main__':
    
    BS = 3
    NO_NO_NO_MELTA = 21
    NO_NO_MELTA = 17
    NO_MELTA = 10
    M_MELTA = 8
    F_MELTA = 5
    N = 100000
    
    RANGE = NO_NO_NO_MELTA
    
    # weapons    
    MultiMelta = ac_weapon.AC_WEAPON(18, 2, BS, 9, 4, 'd6', MELTA = 2)
    HeavyStubber = ac_weapon.AC_WEAPON(36, 3, BS, 4, 0, 1, RAPID_FIRE = 3)    
    
    OpressorCannon = ac_weapon.AC_WEAPON(60, 'd6+3', BS, 12, 2, 3)
    CoaxialAutoCannon = ac_weapon.AC_WEAPON(48, 2, BS, 9, 1, 3)
    PulziverCannon = ac_weapon.AC_WEAPON(24, 'd6', BS, 9, 3, 3)
    MeltaGun = ac_weapon.AC_WEAPON(12, 1, BS, 9, 4, 'd6', MELTA = 2)
    
    # units    
    Just_Dorn = ac_unit.AC_UNIT(10, 12, 2, 0, 18, 7, 5, 
                                  [OpressorCannon, 
                                   CoaxialAutoCannon, 
                                   MultiMelta, 
                                   MultiMelta, 
                                   MeltaGun, 
                                   MeltaGun, 
                                   HeavyStubber, 
                                   PulziverCannon
                                   ], 
                                  #ac_weapon.AC_WEAPON.LETHAL_HITS,
                                  #ac_weapon.AC_WEAPON.PLUS_BS
                                  ac_weapon.AC_WEAPON.IN_COVER,
                                  IGNORE_DAMAGE = 1
                                  )
                                  
    CAD_Dorn = ac_unit.AC_UNIT(10, 12, 2, 0, 18, 7, 5, 
                                  [OpressorCannon, 
                                   CoaxialAutoCannon, 
                                   MultiMelta, 
                                   MultiMelta, 
                                   MeltaGun, 
                                   MeltaGun, 
                                   HeavyStubber, 
                                   PulziverCannon
                                   ], 
                                  ac_weapon.AC_WEAPON.LETHAL_HITS,
                                  #ac_weapon.AC_WEAPON.PLUS_BS
                                  ac_weapon.AC_WEAPON.IN_COVER,
                                  IGNORE_DAMAGE = 1
                                  )
    
    #####
    # DIRECT COMP
    #####
    #save = 3
    #invul = 0
    #toughness = 10
    #target = ac_unit.AC_UNIT(0, toughness, save, invul, 0, 0, 0, [])
    
    #cad_data = CAD_Dorn.get_data_damage_target(target, RANGE, N)
    #just_data = Just_Dorn.get_data_damage_target(target, RANGE, N)
    
    #cad_mean = np.mean(cad_data)
    #just_mean = np.mean(just_data)
    
    #print(cad_mean, just_mean)
    
    #violinplots([cad_data, just_data], plt.gca(), ['CAD', 'Other'], add_text = True)
    #plt.title(f"RogalDorn on T{toughness} and {save}+/{invul}++")
    
    ##plt.show()
    #plt.savefig(f"../rogal_dorn_on_t{toughness}_and_{save}_{invul}.png")
    
    
    #####
    # INST
    #####
    toughnesses = [8, 9, 10, 12, 13]
    save = 3
    invul = 4
    #save = 2
    #invul = 0
    
    CAD_DATAS = []
    JUST_DATAS = []
    
    for t in toughnesses:
        
        target = ac_unit.AC_UNIT(0, t, save, invul, 0, 0, 0, [])
        
        CAD_DATAS.append( CAD_Dorn.get_data_damage_target(target, NO_MELTA, N) )
        JUST_DATAS.append( Just_Dorn.get_data_damage_target(target, NO_MELTA, N) )
        
    
    plot_series([CAD_DATAS, JUST_DATAS], plt.gca(), ['CAD', 'Other'], [f"T{t}" for t in toughnesses], add_cmp_text_on_data = 1)
    
    plt.title(f"RogalDorn on {save}+/{invul}++ and t in {toughnesses}")
    plt.grid()
    
    #plt.show()
    plt.savefig(f"../rogal_dorn_on_{save}_{invul}_on_t_{toughnesses[0]}-{toughnesses[-1]}.png")
        
        
        
        
        
        
    
    
    
