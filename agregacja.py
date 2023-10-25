import numpy as np
import pandas as pd
import random
from scipy.stats import chi
import matplotlib.pyplot as plt
plt.style.use('bmh')

file = open("Tabele_pliki_txt/Agregacja.txt", "w")

def collision_handler(total_size, size_list=None):
    if size_list is None:
        size_list = []
        
    if total_size > 210:
        first_size = random.choice(np.array([30, 60, 90, 120, 150, 180]))
        size_list.append(first_size)
        total_size = total_size - first_size
        collision_handler(total_size, size_list)
    else:
        first_size = total_size
        size_list.append(first_size)
    return size_list

crystal_size = 30
crystal_per_loop = 54

rpm = 120
loops_num = 14 * rpm * 2

crystal_array = np.array([])
df = 3
new_crystals = np.ones(crystal_per_loop) * crystal_size

crystal_number = {}

for _ in range(loops_num):
    file.write(f"Iteracja nr {_}\n")
    crystal_array = np.append(crystal_array, new_crystals)
    np.random.shuffle(crystal_array)
    crystal_series = pd.Series(crystal_array, copy=True)

    x = np.arange(1, len(crystal_array))
    probabils = chi.pdf(x, df, round(len(crystal_array) / 35), len(crystal_array)/10)
    
    if sum(probabils) < 1:
        probabils[0] += 1 - sum(probabils) 
    
    num_to_remove = np.random.choice(x, p=probabils)
    
    if (num_to_remove % 2) != 0:
        num_to_remove += 1
        
    indx_to_remove = random.sample(list(crystal_series.index), num_to_remove.item())
    
    crystals_to_merge = np.array(crystal_series[indx_to_remove], copy=True)
    np.random.shuffle(crystals_to_merge)
    crystals_paired = crystals_to_merge.reshape([-1, 2])
    crystals_merged = []
    for pair in crystals_paired:
        if (pair[0] == 210) or (pair[1] == 210) or(pair[0] + pair[1] > 210):
            destruction_result = collision_handler(np.sum(pair))
            crystals_merged.extend(destruction_result)
        else:
            new_crystal = pair[0] + pair[1]
            crystals_merged.append(new_crystal)
            
    crystals_merged = np.array(crystals_merged)
    crystal_series = crystal_series.drop(indx_to_remove).to_numpy(copy=True)    
    crystal_array = np.append(crystals_merged, crystal_series)

    file.write(f"Przesunięcie dystrybucji Chi: {round(len(crystal_array) / 35)}\n")
    file.write(f"Liczba kryształów zderzających się: {num_to_remove}\n")
    file.write(f"Liczba nowych kryształów ze zderzeń: {len(crystals_merged)}\n")
    file.write(f"Liczba kryształów w układzie: {len(crystal_array)}\n")
    file.write("=================================================\n")

    crystal_number[str(_)] = len(crystal_array)
file.close()

plt.figure(dpi=600, figsize=(6,4))
plt.hist(crystal_array, bins=7, rwidth=0.9)
plt.xlabel("Rozmiar [nm]")
plt.ylabel("Liczba kryształów [-]")
plt.savefig("Wykresy/aglomeracja.png")

iters = list(map(int, list(crystal_number.keys())))
crystal_number = list(crystal_number.values())
plt.figure(dpi=600, figsize=(6,4))
plt.plot(iters, crystal_number)
plt.xlabel("Iteracja")
plt.ylabel("Całkowita liczba kryształów [-]")
plt.savefig("Wykresy/l_kryst_aglomer_iter.png")