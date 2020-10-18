#!/usr/bin/env python
# coding: utf-8

'''
+ Smite, 5wc (+1 each) d3, or d6 if 11+

+ CSM, Infernal Gaze, 5wc, 3d6 - each 4+ mortal
+CSM, Gift of Chaos, 6wc, d6 greater target toughnes, d3+3

+DG, Plague Wind, 5wc, d6 for each model, 6+ mortal
+DG, Curse of the Leper, 7wc, 7d6, mortal for each roll > target toughnes

+ TS, Doombolt, 9wc, d3 mortals
+ TS, TzeenchFirestorm, 7wc, 9d6, 6+ - mortal

+CD, Tz, Bolt of change, 8wc, d3

+CD, Nu, Stream of Corruption, 5wc, d3 if models <10, 10+ - d6

+CD, Slaan, cacophonic choir, 6wc, 2d6 (+2 if result >10) - Ld = mortals

+BA, Bloodboil, wc6, 2d6 > toughnes - d3, 2d6 > 2*toughnes - 3

+SM, Psychic Scourge, wc6, D6+Ld(9) > D6+Ld_opp - d3, if == 1

+DA, Mind Worm, wc6, 1 mortal
+DA, Trephination, wc7, 2d6 (+2 if result >10) - Ld = mortals

+GK, Inner Fire, wc5, d6*numberof result of psytest, for each 3+ - mortal
+GK, Purge soul, wc5, d6+Ld(9) - d6+Ld = numbers of morlals

+Inq, Castigation, wc6, 3d6 > Ld - d3 mortals

+SW, Living Lighing, wc6, d3
+SW, Murderous Hurracane, wc5, 6+ for each unit (model?)
SW, Jaws, wc7, 2d6 - Move = mortals

+IG, Psychic Maelstrom, wc7, 2+ 3+ 4+ 5+ 6+

+Tyr, Psychic Screem, wc5, d3

+Orkz, da krunch, wc8, d6 for each unit, 6 - mortal, then 2d6 if 10+, roll again d6 for each anf 6 mortal

+Eld, Mind War, wc7, d6+LD - d6_Ld = mortals
+Eld, Executioner, wc7, d3, if model slain + d3

Harl, Mirror of Minds, wc7, bith roll d6, if >= mortal, repeat until < or destroyed
Harl, Shards of lights wc7, d3

+Innary, Gaze of Ynnead, wc6, d6: 1- mortal, 2-5 - d3, 6 - d6

+Gen, Psionic Blast, wc5, 2d6 < Ld - 1 mortal, >= LD - d3
Gen, Mental Onslaught, wc6, d6+Ld > d6+Ld - mortal, repeat until 6 or =<
'''

import numpy as np
import ac_core
import matplotlib.pyplot as plt

class Psychic_power(object):
    def __init__(self, name, wc):
        self.wc = wc        
        self.name = name
        
    def cast(self, wc = None):
        psi_test = ac_core.d6() + ac_core.d6()
        if wc is None:
            #if self.wc = None:
                #print("Power {} is not well defined!", self.name)
                #return None, None            
            if psi_test >= self.wc:
                return True, psi_test
            return False, psi_test            
        else:
            if psi_test >= wc:
                return True, psi_test
            return False, psi_test
    
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):
        print("Power {} has no get_damage function implemented".format(self.name))
        return -1
    
    def test_power(self, N = 10000, wc = None, ld = None, m = None, w = None, t = None):
        results = []        
        for i in range(N):
            results.append(self.get_damage(wc, ld, m, w, t))
            
        name = self.name
        if wc is not None:
            name += " wc={}".format(wc)
        if ld is not None:
            name += " ld={}".format(ld)
        if m is not None:
            name += " m={}".format(m)
        if w is not None:
            name += " w={}".format(w)
        if t is not None:
            name += " t={}".format(t)
            
        return results, name

#
# POWERS WITHOUT STATS DEPENDANCE
#

class Smite(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, "Smite", 5)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        if pt1:
            if pt2 > 10:
                return ac_core.d6()
            return ac_core.d3()
        return 0        
        
class Infernal_gaze(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Infernal gaze', 5)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(3):
                if ac_core.d6() >= 4:
                    d+=1
        return d                    
                
class JustD3(Psychic_power):
    def __init__(self, name, wc):
        Psychic_power.__init__(self, name, wc)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        if pt1:
            return ac_core.d3()
        return 0
    
class Doombolt(JustD3):
    def __init__(self):
        JustD3.__init__(self, 'Doombolt', 9)


class Living_lightning(JustD3):
    def __init__(self):
        JustD3.__init__(self, 'Living lightning', 6)

class Psychic_scream(JustD3):
    def __init__(self):
        JustD3.__init__(self, 'Psychic scream', 5)

class Bolt_of_change(JustD3):
    def __init__(self):
        JustD3.__init__(self, 'Bolt of change', 8)

class Tzeench_firestorm(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Tzeench firestorm', 7)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(9):
                if ac_core.d6() == 6:
                    d+=1
        return d

class Psychic_maelstorm(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Psychic maelstorm', 7)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(5):
                if( ac_core.d6() >= i+2):
                    d += 1
                else:
                    break
        return d

class Gaze_of_Ynnead(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Gaze of Ynnead', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r = ac_core.d6()
            if r == 1:
                d = 1
            elif r == 6:
                d = ac_core.d6()
            else:
                d = ac_core.d3()
        return d


class Mindworm(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Mindworm', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            d = 1
        return d

class Inner_fire(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Inner fire', 5)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(pt2):
                if ac_core.d6() > 2:
                    d+=1
        return d

#
# POWERS DEPENDED ON MODEL WOUND CHARACTERISTIC
#

class Executioner(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Executioner', 7)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if w is None:
            print("Error! Provide wound number for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            d = ac_core.d3()
            if d >= w:
                d += ac_core.d3()
        return d


#
# POWERS DEPENDED ON MODELS IN UNIT
#

class Plague_wind(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Plague Wind\Murderous huracane', 5)
            
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if m is None:
            print("Error! Provide model number for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(m):
                if ac_core.d6() == 6:
                    d += 1
        return d
                    
class Da_krunch(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Da krunch!', 8)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if m is None:
            print("Error! Provide model number for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(m):
                if ac_core.d6() == 6:
                    d += 1
            r = ac_core.d6() + ac_core.d6()
            if r >= 10:
                for i in range(m):
                    if ac_core.d6() == 6:
                        d += 1
                    
        return d

class Stream_of_corruption(Psychic_power):
    def __init__(self):
       Psychic_power.__init__ (self, 'Stream of corruption', 5)
       
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if m is None:
            print("Error! Provide model number for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            if m < 10:
                d = ac_core.d3()
            else:
                d = ac_core.d6()
        return d
        
#
# POWERS DEPENDED ON MODELS TOUGHNESS
#

class Curse_of_the_Leper(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Curse of the Leper', 7)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if t is None:
            print("Error! Provide toughness for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            for i in range(7):
                if ac_core.d6() > t:
                    d+=1
        return d

class Gift_of_Chaos(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, '*Gift of Chaos', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if t is None:
            print("Error! Provide toughness for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            if ac_core.d6() > t:
                d = ac_core.d3() + 3
        return d

class Bloodboil(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Bloodboil', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if t is None:
            print("Error! Provide toughness for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r = ac_core.d6() + ac_core.d6()
            if r > t *2:
                d = 3
            elif r > t:
                d = ac_core.d3()
        return d

#
# POWERS DEPENDED ON MODELS LEADERSHIP
#

class Purge_soul(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Purge soul', 5)

    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r1 = 9 + ac_core.d6()
            r2 = ld + ac_core.d6()
            d = r1 - r2
            if d < 0:
                d = 0
        return d

class Mind_war(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Mind war', 7)

    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r1 = 9 + ac_core.d6()
            r2 = ld + ac_core.d6()
            d = r1 - r2
            if d < 0:
                d = 0
        return d
    
class Cacophonic_choir(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Cacophonic choir', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r = ac_core.d6() + ac_core.d6()
            if pt2 > 10:
                r +=2
            d = r - ld
            if d < 0:
                d = 0
        return d

class Trephination(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Trephination', 7)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r = ac_core.d6() + ac_core.d6()
            if pt2 > 10:
                r +=2
            d = r - ld
            if d < 0:
                d = 0
        return d

class Castigation(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Castigation', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r = ac_core.d6()+ac_core.d6()+ac_core.d6()
            if r > ld:
                d = ac_core.d3()
                
        return d

class Psychic_scourge(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Psychic scourge', 6)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r1 = ac_core.d6() + 9
            r2 = ac_core.d6() + ld
            if r1 == r2:
                d = 1
            elif r1 > r2:
                d = ac_core.d3()
        return d
    
class Psionic_blast(Psychic_power):
    def __init__(self):
        Psychic_power.__init__(self, 'Psionic blast', 5)
        
    def get_damage(self, wc = None, ld = None, m = None, w = None, t = None):        
        if ld is None:
            print("Error! Provide Ld for {} power!".format(self.name))
        pt1, pt2 = self.cast(wc)
        d = 0
        if pt1:
            r = ac_core.d6() + ac_core.d6()            
            if r < ld:
                d = 1
            else:
                d = ac_core.d3()
        return d
        
if __name__ == '__main__' :
    
    all_powers = {}
    
    def add_power( results ):
        (d, l) = results        
        all_powers[l] = d
    
    ld_powers = {}
    lds = [5,6,7,8,9,10]
    def add_ld_power( results ):
        (d, l) = results
        ld_powers[l] = d
    
    smite = Smite()    
    add_power( smite.test_power() )
    add_power( smite.test_power(wc = 6) )
    add_power( smite.test_power(wc = 7) )
    infernal_gaze = Infernal_gaze()
    add_power( infernal_gaze.test_power() )
    
    db = Doombolt()
    add_power( db.test_power() )
    
    ll = Living_lightning()
    add_power( ll.test_power() )
    
    ps = Psychic_scream()
    add_power( ps.test_power() )
    
    tf = Tzeench_firestorm()
    add_power( tf.test_power() )
    
    boc = Bolt_of_change()
    add_power( boc.test_power() )
    
    pm = Psychic_maelstorm()
    add_power( pm.test_power() )
    
    goy = Gaze_of_Ynnead()
    add_power( goy.test_power() )
    
    mw = Mindworm()
    add_power( mw.test_power() )
    
    if_ = Inner_fire()
    add_power( if_.test_power() )
    
    e = Executioner()
    add_power( e.test_power(w = 1) )
    add_power( e.test_power(w = 2) )
    add_power( e.test_power(w = 3) )
    add_power( e.test_power(w = 4) )
    
    pw = Plague_wind()
    add_power( pw.test_power(m = 5) )
    add_power( pw.test_power(m = 10) )
    
    dk = Da_krunch()
    add_power( dk.test_power(m = 5) )
    add_power( dk.test_power(m = 10) )
    
    soc = Stream_of_corruption()
    add_power( soc.test_power(m = 5) )
    add_power( soc.test_power(m = 10) )
    
    cotl = Curse_of_the_Leper()
    add_power( cotl.test_power(t = 3) )
    add_power( cotl.test_power(t = 4) )
    
    goc = Gift_of_Chaos()
    add_power( goc.test_power(t = 3) )
    add_power( goc.test_power(t = 4) )
    
    bb = Bloodboil()
    add_power( bb.test_power(t = 3) )
    add_power( bb.test_power(t = 4) )
    
    # LD
    ps = Purge_soul()
    add_power( ps.test_power(ld = 6) )
    add_power( ps.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( ps.test_power(ld = ld))
    
    mw = Mind_war()
    add_power( mw.test_power(ld = 6) )
    add_power( mw.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( mw.test_power(ld = ld))
    
    cc = Cacophonic_choir()
    add_power( cc.test_power(ld = 6) )
    add_power( cc.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( cc.test_power(ld = ld))
    
    t = Trephination()
    add_power( t.test_power(ld = 6) )
    add_power( t.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( t.test_power(ld = ld))
    
    c = Castigation()
    add_power( c.test_power(ld = 6) )
    add_power( c.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( c.test_power(ld = ld))
    
    ps_ = Psychic_scourge()
    add_power( ps_.test_power(ld = 6) )
    add_power( ps_.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( ps_.test_power(ld = ld))
    
    pb = Psionic_blast()
    add_power( pb.test_power(ld = 6) )
    add_power( pb.test_power(ld = 9) )
    for ld in lds:
        add_ld_power( pb.test_power(ld = ld))
        
    
    # all
    fig1, ax1 = plt.subplots()    
    all_powers = {k: v for k, v in sorted(all_powers.items(), key=lambda item: np.mean(item[1]))}    
    ac_core.boxplot(list(all_powers.values()), ax1, list(all_powers.keys()), rotation = 90)
    plt.title('Psychic powers top')    
    plt.ylabel("Mortal  wounds inflicted")
    plt.xlabel("Powers")
    fig1.autofmt_xdate()
    plt.grid()
    plt.show()
    
    # ld
    fig1, ax1 = plt.subplots()    
    for i in range(7):
        list(ld_powers.values())[i*len(lds):(i+1)*len(lds)]
        plt.plot(lds, , label=list(ld_powers.keys())[0][0:-4] )
    plt.grid()
    plt.show()
    
    fig1, ax1 = plt.subplots()    
    ld_powers = {k: v for k, v in sorted(ld_powers.items(), key=lambda item: np.mean(item[1]))}    
    ac_core.boxplot(list(ld_powers.values()), ax1, list(ld_powers.keys()), rotation = 90)
    plt.title('Psychic powers (leadership) top')    
    plt.ylabel("Mortal  wounds inflicted")
    plt.xlabel("Powers")
    fig1.autofmt_xdate()
    plt.grid()
    plt.show()

