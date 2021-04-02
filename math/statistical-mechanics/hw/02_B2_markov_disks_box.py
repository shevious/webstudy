import random, pylab

L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
sigma = 0.1197
sigma_sq = sigma ** 2
delta = 0.1

def markov_disks_box():
    a = random.choice(L)
    b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
    box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
    if not (box_cond or min_dist < 4.0 * sigma ** 2):
        a[:] = b
    return L


N = 4
n_steps = 2000000
histo_data = []
for run in range(n_steps):
    pos = markov_disks_box()
    for k in range(N):
        histo_data.append(pos[k][0])
#pylab.hist(histo_data, bins=100, normed=True)
pylab.hist(histo_data, bins=100, density=True)
pylab.xlabel('x')
pylab.ylabel('frequency')
pylab.title('Markov chain: x coordinate histogram (density eta=0.18)')
pylab.grid()
pylab.savefig('markov_disks_histo.png')
pylab.show()
