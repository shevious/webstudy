import random
import math

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  math.sqrt(d_x**2 + d_y**2)

L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
sigma = 0.15
sigma_sq = sigma ** 2
delta = 0.1
n_steps = 1000
for steps in range(n_steps):
    a = random.choice(L)
    b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    # periodic boundary condition
    b[0] = b[0] % 1.0
    b[1] = b[1] % 1.0
    # set initial distance large enought
    min_dist = 4
    for c in L:
      if c == a:
        continue
      for ix in range(-1, 2):
        for iy in range(-1, 2):
          d = [c[0]+ix, c[1]+iy]
          min_dist = min(min_dist, dist(b, d))
    if not (min_dist < 2.0 * sigma):
        a[:] = b
print(L)
