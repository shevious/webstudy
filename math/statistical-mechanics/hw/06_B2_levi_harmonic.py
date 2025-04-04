import math, random, pylab

def levy_harmonic_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
               1.0 / math.sqrt(Ups1)))
    return x

beta = 20.0
N = 80
dtau = beta / N
delta = 1.0
n_steps = 40000
x = [0.0] * N
data = []
for step in range(n_steps):
    x = levy_harmonic_path(x[0], x[0], dtau, N)
    k = random.randint(0, N - 1)
    data.append(x[k])
    Ncut = N//2
    x = x[Ncut:] + x[:Ncut] 

# graphics
'''
y = [j * dtau for j in range(N)]
pylab.plot(x, y, 'b-')
pylab.xlabel('$x$', fontsize=18)
pylab.ylabel('$\\tau$', fontsize=18)
pylab.title('Levi harmonic path, N= %i, $\\beta$ = %.0f'%(N, beta))
pylab.xlim(-3.0, 3.0)
pylab.savefig('plot_B2_levi_path_beta%s.png' % beta)
pylab.show()
'''

pylab.hist(data, density=True, bins=100, label='Levi-path')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
          math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
pylab.plot(list_x, list_y, label='analytic')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
pylab.title('levi_harmonic_path (beta=%s, N=%i)' % (beta, N))
pylab.xlim(-2, 2)
pylab.savefig('plot_B2_levi_beta%s.png' % beta)
pylab.show()
