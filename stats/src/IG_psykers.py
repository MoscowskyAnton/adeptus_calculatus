import numpy as np
import ac_core
import matplotlib.pyplot as plt

def primaris_smite(bonus = 0, wc = 5):
    damage = 0
    test = ac_core.d6() + ac_core.d6() + bonus
    if test > 10:
        damage = ac_core.d6()
    elif test > wc:
        damage = ac_core.d3()
    return damage
        
def wyrdvane_smite(bonus = 0, wc = 5, wyrd_bonus = 0):
    damage = 0
    test = ac_core.d6() + bonus + wyrd_bonus
    if test > 10:
        damage = ac_core.d6()
    elif test > wc:
        damage = ac_core.d3()
    return damage

if __name__ == '__main__' :
    
    N = 100000
    all_exps = {}
    
    all_exps["P_3W"] = []
    all_exps["3W_P"] = []
    all_exps["P_3W_str"] = []
    all_exps["3W_P_str"] = []
    all_exps["P_2W"] = []
    all_exps["2W_P"] = []
    all_exps["P_2W_str"] = []
    all_exps["2W_P_str"] = []    
    
    for i in range(N):        
        
        all_exps["P_3W"].append(primaris_smite(0,5) + wyrdvane_smite(0,6,1))
        all_exps["3W_P"].append(primaris_smite(0,6) + wyrdvane_smite(0,5,1))
        all_exps["P_3W_str"].append(primaris_smite(2,5) + wyrdvane_smite(2,6,1))
        all_exps["3W_P_str"].append(primaris_smite(2,6) + wyrdvane_smite(2,5,1))
        all_exps["P_2W"].append(primaris_smite(0,5) + wyrdvane_smite(0,6))
        all_exps["2W_P"].append(primaris_smite(0,6) + wyrdvane_smite(0,5))
        all_exps["P_2W_str"].append(primaris_smite(2,5) + wyrdvane_smite(2,6))
        all_exps["2W_P_str"].append(primaris_smite(2,6) + wyrdvane_smite(2,5))
        
    all_exps = {k: v for k, v in sorted(all_exps.items(), key=lambda item: np.mean(item[1]))}    
    
    fig1, ax1 = plt.subplots()        
    ac_core.boxplot(list(all_exps.values()), ax1, list(all_exps.keys()))
    plt.grid()
    plt.title("Smites in Imperial Guard")
    plt.ylabel("Infilicted mortals")
    plt.xlabel("Sequence")
    fig1.autofmt_xdate()
    plt.show()
    
        
