import random, math, pylab

x = 0.0
delta = 0.5
data = []

def psi_0_sq(x):
    return math.exp(-x**2)/math.sqrt(math.pi)

for k in range(50000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) < psi_0_sq(x_new)/psi_0_sq(x):
        x = x_new 
    data.append(x)

pylab.hist(data, 100, density = 'True', label='histogram')
x = [a / 10.0 for a in range(-50, 51)]
y = [psi_0_sq(a) for a in x]
pylab.plot(x, y, c='red', linewidth=2.0, label='anlaytic curve')
pylab.title('Ground state of quantum harmonic oscillator \
    \nnormalized histogram for '+str(len(data))+' samples', fontsize = 10)
pylab.xlabel('$x$', fontsize = 15)
pylab.ylabel('$|\Psi_0(x)|^2$', fontsize = 15)
pylab.legend()
pylab.savefig('plot_markov_harmonic.png')
pylab.show()
