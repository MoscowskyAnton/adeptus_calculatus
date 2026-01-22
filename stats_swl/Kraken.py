import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Определение кубиков (8 граней)
def get_white_die():
    return ['blank']*6 + ['hit']*1 + ['crit']*1

def get_black_die():
    return ['blank']*4 + ['hit']*3 + ['crit']*1

def get_red_die():
    return ['blank']*2 + ['hit']*5 + ['crit']*1

white_faces = get_white_die()
black_faces = get_black_die()
red_faces = get_red_die()

# Базовый состав отряда (всего 16 моделей)
leader_black = 1
leader_white = 1
special_black = 3
normal_white = 13
total_models = 1 + 1 + 1 + 13  # 16

def get_dice_pool(killed):
    # Начальный пул
    whites = leader_white + normal_white  # 14 белых
    blacks = leader_black + special_black  # 4 черных
    reds = 0

    whites = whites - killed

    new_blacks = 0

    # Применяем улучшения
    for i in range(killed):
        if blacks > 0:
            blacks -= 1
            reds += 1
        elif whites > 0:
            whites -= 1
            new_blacks += 1

    return reds, blacks + new_blacks, whites

def simulate_attack(reds, blacks, whites, aims = 0, n_simulations=100000):
    """Симулирует N бросков и возвращает среднее и std для хитов и критов"""
    total_hits = []
    total_crits = []


    for _ in range(n_simulations):
        hits = 0
        crits = 0

        rerolls = aims * 2

        # Красные кубики
        for _ in range(reds):
            face = np.random.choice(red_faces)
            if (face == 'blank' or face == 'surge') and rerolls > 0:
                face = np.random.choice(red_faces)
                rerolls -= 1
            if face == 'hit': hits += 1
            if face == 'crit': crits += 1

        # Черные кубики
        for _ in range(blacks):
            face = np.random.choice(black_faces)
            if (face == 'blank' or face == 'surge') and rerolls > 0:
                face = np.random.choice(black_faces)
                rerolls -= 1
            if face == 'hit': hits += 1
            if face == 'crit': crits += 1

        # Белые кубики
        for _ in range(whites):
            face = np.random.choice(white_faces)
            if (face == 'blank' or face == 'surge') and rerolls > 0:
                face = np.random.choice(white_faces)
                rerolls -= 1
            if face == 'hit': hits += 1
            if face == 'crit': crits += 1

        total_hits.append(hits)
        total_crits.append(crits)

    return (np.mean(total_hits), np.std(total_hits)),(np.mean(total_crits), np.std(total_crits))

# Основной расчет
N_SIMULATIONS = 100000
results_hits = []
results_crits = []
killed_range = range(0, 14)
AIMS = 1

print("Расчет эффективности отряда дроидов B1 по числу убитых моделей:")
print("Killed | Avg Hits ± Std  | Avg Crits ± Std")
print("-" * 45)

for killed in killed_range:
    reds, blacks, whites = get_dice_pool(killed)
    (hits_mean, hits_std), (crits_mean, crits_std) = simulate_attack(reds, blacks, whites, aims = AIMS, n_simulations=N_SIMULATIONS)

    results_hits.append((hits_mean, hits_std))
    results_crits.append((crits_mean, crits_std))

    print(f"{killed:6} | {hits_mean:8.2f} ± {hits_std:4.2f} | {crits_mean:8.2f} ± {crits_std:4.2f}")

# Построение графика
x = np.arange(len(killed_range))
width = 0.8

fig, ax = plt.subplots(figsize=(12, 8))

# Столбики для хитов (нижние)
hits_means = [h[0] for h in results_hits]
hits_stds = [h[1] for h in results_hits]
bars1 = ax.bar(x, hits_means, width, label='Хиты', color='grey', alpha=0.8)

# Столбики для критов (верхние, сложенные на хиты)
crits_means = [c[0] for c in results_crits]
crits_stds = [c[1] for c in results_crits]
bars2 = ax.bar(x, crits_means, width, bottom=hits_means, label='Криты', color='blue', alpha=0.8)

# Ошибки (вертикальные полоски)
# ax.errorbar(x, np.array(hits_means)+np.array(crits_means)/2,
#            yerr=np.sqrt(np.array(hits_stds)**2 + np.array(crits_stds)**2),
#            fmt='k.', capsize=5, capthick=1.5, label='Разброс')

ax.errorbar(x - width/4, np.array(hits_means),
           yerr=np.sqrt(np.array(hits_stds)**2),
           fmt='k.', capsize=5, capthick=1.5)

ax.errorbar(x + width/4, np.array(crits_means)  + np.array(hits_means),
           yerr=np.sqrt(np.array(crits_stds)**2),
           fmt='k.', capsize=5, capthick=1.5)

# Настройка графика
ax.set_xlabel('Число убитых моделей')
ax.set_ylabel('Среднее количество результатов')
ax.set_title(f'Эффективность блоба дроидов B1 с Кракеном и Е-5С (SWL) AIM={AIMS}')
ax.set_xticks(x)
ax.set_xticklabels(killed_range)
ax.legend()
ax.grid(True, alpha=0.3)

# Добавление значений на столбики
for i, (h_mean, c_mean) in enumerate(zip(hits_means, crits_means)):
    ax.text(i, h_mean/2, f'{h_mean:.2f}', ha='center', va='center', fontweight='bold')
    ax.text(i, h_mean + c_mean/2, f'{c_mean:.2f}', ha='center', va='center',
            fontweight='bold', color='black')


# Вывод итоговой таблицы
print("\nИтоговая таблица:")
print("Убито | Хиты | Криты | Всего урона | Состав кубиков")
print("-" * 50)
for i, killed in enumerate(killed_range):
    reds, blacks, whites = get_dice_pool(killed)
    total_damage = results_hits[i][0] + results_crits[i][0]
    print(f"{killed:6} | {results_hits[i][0]:4.1f} | {results_crits[i][0]:4.1f} | "
          f"{total_damage:9.1f} | R{reds} B{blacks} W{whites}")

plt.tight_layout()
plt.show()
