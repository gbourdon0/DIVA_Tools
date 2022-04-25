from modules.data_reader.pickle_reader import PickleReader as pr
import pandas as pd
import numpy as np
a = np.zeros((4,4))
k = 0
for i in range(len(a)):
    for j in range(len(a[i])):
        a[i][j] = k
        k+=1
select = []