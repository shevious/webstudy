import numpy as np

def pow(n):
  if (n >= 1):
    return 2*pow(n-1)
  else:
    return np.array(1, dtype=int)

def sum_pow(n):
  sum = np.array(0, dtype=int)
  for i in range(0, n+1, 1):
    sum += pow(i)
  return sum

for i in range(0, 68, 1):
  print(i, sum_pow(i))

