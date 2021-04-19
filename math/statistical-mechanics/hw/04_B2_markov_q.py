import random
import math
import pylab

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

n_trials = 5000000
d = 4

delta = 0.05
print('n_trials =', n_trials)

x = [0]*(d-1)
old_radius_square = 0

n_hits = 0
for i in range(n_trials):
    k = random.randint(0, d-2)
    alpha = random.uniform(-1, 1)
    x_old_k = x[k]
    x_new_k = x_old_k + random.uniform(-delta, delta)
    new_radius_square = old_radius_square + x_new_k**2 - x_old_k**2
    if (new_radius_square < 1):
        x[k] = x_new_k
        old_radius_square = new_radius_square
    if (new_radius_square + alpha**2 < 1):
        n_hits += 1

Q_avg = 2.0 * n_hits / float(n_trials)


print('<Q> =', Q_avg)
print('V_sph(%i)/V_sph(%i) = %f'%(d, d-1, V_sph(d)/V_sph(d-1)))
