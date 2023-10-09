import numpy as np
import pandas as pd

rpm = 120
loops_num = 14 * rpm

crystal_table = pd.Series([], dtype=np.int32)

crystal_table.append((30, 30, 30, 30))