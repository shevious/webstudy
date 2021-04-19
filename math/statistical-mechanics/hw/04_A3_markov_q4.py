import random
import math

n_trials = 10000000
delta = 0.1
print('n_trials =', n_trials)


x, y, z = 0.0, 0.0, 0.0
n_hits = 0
for i in range(n_trials):
    del_x, del_y, del_z = random.uniform(-delta, delta), random.uniform(-delta, delta), random.uniform(-delta, delta)
    alpha = random.uniform(-1, 1)
    if (x + del_x)**2 + (y + del_y)**2 + (z + del_z)**2 < 1.0:
        x, y, z = x + del_x, y + del_y, z + del_z
    if x**2 + y**2 + z**2 + alpha**2 < 1.0: n_hits += 1

Q_4_avg = 2.0 * n_hits / float(n_trials)
print('Q_4_exact = ', (3./8.)*math.pi)
print('<Q_4> = ', Q_4_avg)

x, y = 0.0, 0.0
n_hits = 0
for i in range(n_trials):
    del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
    z = random.uniform(-1, 1)
    if (x + del_x)**2 + (y + del_y)**2 < 1.0:
        x, y = x + del_x, y + del_y
    if x**2 + y**2 + z**2 < 1.0: n_hits += 1

Q_3_avg = 2.0 * n_hits / float(n_trials)
print('<Q_3> = ', Q_3_avg)

print('V_sph(4) =', math.pi**2/2.)
print('V_sph(3)*<Q_4> =', (4./3.)*math.pi*Q_4_avg)
print('V_sph(2)*<Q_3><Q_4> =', math.pi*Q_3_avg*Q_4_avg)
