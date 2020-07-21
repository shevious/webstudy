import numpy as np
x = np.array([[ 1.0, 1.1 ], [ 2.0, 2.1 ], [ 1.0, 1.1 ]])

y = x
y = y*2 # or y *= 2

print(y)

y = x*2

print(y)

y = x[:, 1:]*2
print(y)

#x[:, :0] *= 2
#print(x)
print(x[:, 1:2] )
