import pandas as pd
import numpy as np
from glob import glob
import os

folder = '.'
file_names = glob(os.path.join(folder, '*/*.xlsx'))
file_name = file_names[0]

print(file_name)
data_all = pd.read_excel(file_name)
print(data_all.head())

