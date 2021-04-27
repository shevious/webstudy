import math, random, pylab
import numpy

def levy_free_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        x_mean = (dtau_prime * x[k - 1] + dtau * xend) / \
                 (dtau + dtau_prime)
        sigma = math.sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
        x.append(random.gauss(x_mean, sigma))
    return x

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

def V(x, cubic, quartic):
    pot = x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4
    return pot

beta = 20.0
N = 100
dtau = beta / N
delta = 1.0
n_steps = 500000
x = [0.0] * N
data = []

Ncut = 20
quartic = 1
cubic = -quartic

x = levy_free_path(x[0], x[0], dtau, N)
Trotter_weight_old = math.exp(sum(-V(a, cubic, quartic) * dtau for a in x))

count =0

for step in range(n_steps):
    x_new = levy_free_path(x[0], x[Ncut], dtau, Ncut) + x[Ncut:]
    Trotter_weight_new = math.exp(sum(-V(a, cubic, quartic) * dtau for a in x_new))
    if random.uniform(0, 1) < Trotter_weight_new/Trotter_weight_old:
        Trotter_weight_old = Trotter_weight_new
        x = x_new[:]
        count += 1
    x = x[1:] + x[:1]
    k = random.randint(0, N - 1)
    data.append(x[k])

  
# matrix-sqauring

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
          math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
          numpy.exp(-0.5 * beta * (V(x, cubic, quartic) + V(xp, cubic, quartic))) \
          for x in grid] for xp in grid])

x_max = 5.0
nx = 200
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-(nx - 1) // 2, nx // 2 + 1)]
beta_tmp = 20/(2.0 ** (8))            # initial value of beta (power of 2)
beta     = 20.                      # actual value of beta (power of 2)
rho = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
while beta_tmp < beta:
    rho = numpy.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0

Z = sum(rho[j, j] for j in range(nx + 1)) * dx
pi_of_x = [rho[j, j] / Z for j in range(nx + 1)]

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

pylab.hist(data, density=True, bins=200, label='Levi-path')
pylab.plot(x, pi_of_x, label='matrix-square')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
          math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
#pylab.plot(list_x, list_y, label='analytic')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
pylab.title('metro_levi_free_anharmonic\n(beta=%s, N=%i, n_steps=%i, Ncut=%i)' % (beta, N, n_steps, Ncut))
pylab.xlim(-2, 2)
pylab.savefig('plot_C1_metro_levi_free.png')
pylab.show()
