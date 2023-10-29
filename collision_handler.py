import random
import numpy as np

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