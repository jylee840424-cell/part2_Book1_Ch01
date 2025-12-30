import numpy as np
import pandas as pd
import matplotlib as plt

print("np.__version__",np.__version__)
print("np.__version__",pd.__version__)
print("ok")


num_list = [1,2,3,4,5]
print(num_list)  # 파이썬 기본 List
data = np.array(num_list)
print(data) # 넘파이 Array
print(data.mean())
print(data.max())