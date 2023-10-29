import numpy as np
from scipy.stats import chi

def probability_generator(crystal_array, df):
    x = np.arange(1, len(crystal_array))
    probabils = chi.pdf(x, df, round(len(crystal_array) / 35), len(crystal_array)/10)
    
    if sum(probabils) < 1:
        probabils[0] += 1 - sum(probabils)
    return x, probabils