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

d = 20
n_runs = 10

V_sph_exact = V_sph(d)

V_sph_list = []
for k in range(1, 6):
    n_trials = 10**k
    V_sph_avg = 0.
    V_sph_sq_avg = 0.
    for i in range(n_runs):
        V_sph_est = V_sph_iter(d, n_trials)
        V_sph_list.append(V_sph_est)
        V_sph_avg += V_sph_est
        V_sph_sq_avg += V_sph_est**2
    V_sph_avg = V_sph_avg/n_runs
    V_sph_sq_avg = V_sph_sq_avg/n_runs
    error = math.sqrt(V_sph_sq_avg - V_sph_avg**2)/math.sqrt(n_runs)
    difference = V_sph_avg - V_sph_exact
    print('%i | %e | %e | %e | %e'%(n_trials, V_sph_avg, V_sph_exact, error, difference))
        
    

