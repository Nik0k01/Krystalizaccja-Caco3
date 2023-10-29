import numpy as np
import pandas as pd
import random
from probability_generator import probability_generator
from aglomer_plot import aglomer_plot
from collision_handler import collision_handler

file = open("Tabele_pliki_txt/Agregacja.txt", "w")

crystal_size = 30
crystal_per_loop = 1000

rpm = 120
loops_num = 7 * rpm * 2

crystal_array = np.array([])
df = 3
new_crystals = np.ones(crystal_per_loop) * crystal_size

crystal_number = {}

for _ in range(loops_num):
    file.write(f"Iteracja nr {_}\n")
    crystal_array = np.append(crystal_array, new_crystals)
    np.random.shuffle(crystal_array)
    crystal_series = pd.Series(crystal_array, copy=True)

    x, probabils = probability_generator(crystal_array, df) 
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
aglomer_plot(crystal_array, crystal_number)