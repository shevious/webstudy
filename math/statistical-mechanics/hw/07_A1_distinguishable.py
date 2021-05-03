import math, random, pylab

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def pi_x(x, beta):
    sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
    return math.exp(-x ** 2 / (2.0 * sigma ** 2)) / math.sqrt(2.0 * math.pi) / sigma

beta = 2.0
nsteps = 1000000
low = levy_harmonic_path(2)
high = low[:]
data = []

particle_id = 0

for step in range(nsteps):
    k = random.choice([0, 1])
    low[k] = levy_harmonic_path(1)[0]
    high[k] = low[k]
    data += low[:]
        
# analytic curve

list_x = [0.1 * a for a in range (-30, 31)]
list_y = [pi_x(x, beta) for x in list_x]

pylab.title('Two distinguishable particles\n' +
            'nsteps = %i, $\\beta$ = %.0f'%(nsteps, beta))
pylab.hist(data, bins=200, density=True, label='histogram')
pylab.plot(list_x, list_y, label='analytic')
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
pylab.xlim(-3, 3)
pylab.legend()
pylab.show()
