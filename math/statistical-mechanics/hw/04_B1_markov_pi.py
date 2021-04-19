import random
import math
import pylab

n_trials = 500000
d = 4

delta = 0.1
print('n_trials =', n_trials)

x = [0]*d
old_radius_square = 0
r = []

n_hits = 0
for i in range(n_trials):
    k = random.randint(0, d-1)
    x_old_k = x[k]
    x_new_k = x_old_k + random.uniform(-delta, delta)
    new_radius_square = old_radius_square + x_new_k**2 - x_old_k**2
    if (new_radius_square < 1):
        x[k] = x_new_k
        old_radius_square = new_radius_square
    r.append(math.sqrt(old_radius_square))

pylab.title('Efficient sampling: d = %i, n_trials = %i'%(d, n_trials))
pylab.xlabel('radius')
pylab.ylabel('frequency')
pylab.hist(r, bins=100, density=True)
if d == 4:
    pylab.plot([r/100. for r in range(100)], [4*(r/100.)**3 for r in range(100)])
elif d == 20:
    pylab.plot([r/100. for r in range(100)], [20*(r/100.)**19 for r in range(100)])
pylab.show()

