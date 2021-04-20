import random
import math
import pylab

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

n_trials = 100000

delta = 0.05

def Q_avg(d, n_trials):
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
    return Q_avg


def V_sph_iter(d, n_trials):
    if d == 1:
        return 2
    val =  V_sph_iter(d-1, n_trials)*Q_avg(d, n_trials)
    return val

d = 200

V_sph_exact = V_sph(d)
V_sph_est = V_sph_iter(d, n_trials)

print('V_sph(%i) estimated = %e'%(d, V_sph_est))
print('V_sph(%i) exact = %e'%(d, V_sph_exact))
