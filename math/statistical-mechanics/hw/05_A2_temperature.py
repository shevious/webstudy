import random, math, pylab

x = 0.01
delta = 1.0
data = []
n = 1
#beta = 0.2
#beta = 1
beta = 5

def psi_n_square(x, n):
    if n == -1:
        return 0.0
    else:
        psi = [math.exp(-x ** 2 / 2.0) / math.pi ** 0.25]
        psi.append(math.sqrt(2.0) * x * psi[0])
        for k in range(2, n + 1):
            psi.append(math.sqrt(2.0 / k) * x * psi[k - 1] -
                       math.sqrt((k - 1.0) / k) * psi[k - 2])
        return psi[n] ** 2

#pi_quant(x) = sqrt[ tanh(beta/2) / pi] exp[ - x^2 * tanh(beta/2) ]
def pi_quant(x):
    return math.sqrt(math.tanh(beta/2)/math.pi)*math.exp(-x**2*math.tanh(beta/2))

#pi_class(x) = sqrt[beta/ (2 pi)] exp(- beta x^2/ 2)
def pi_class(x):
    return math.sqrt(beta/(2*math.pi))*math.exp(-beta*x**2/2)

for k in range(100000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) < psi_n_square(x_new, n)/psi_n_square(x, n):
        x = x_new 
    data.append(x)
    m = n + random.choice([1, -1])
    if random.uniform(0.0, 1.0) < \
        psi_n_square(x, m)/psi_n_square(x, n)*math.exp(-beta*(m-n)):
        n = m

pylab.hist(data, 100, density = 'True', label='histogram')
x = [a / 10.0 for a in range(-70, 71)]
y = [pi_quant(a) for a in x]
pylab.plot(x, y, c='red', linewidth=2.0, label='analytic quantum prob.')
y = [pi_class(a) for a in x]
pylab.plot(x, y, c='green', linewidth=2.0, label='analytic classical prob.')
pylab.title('Quantum harmonic oscillator finite temperature \
    \n' + str(len(data))+' samples, '+'delta = %.1f, '%(delta)+'$\\beta$ = %.1f'%(beta), fontsize = 10)
pylab.xlabel('$x$', fontsize = 15)
pylab.ylabel('Probability', fontsize = 15)
pylab.legend()
pylab.savefig('plot_markov_harmonic.png')
pylab.show()
