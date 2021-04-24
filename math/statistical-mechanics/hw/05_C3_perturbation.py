import math, numpy, pylab


# Energy perturbation
def Energy_pert(n, cubic, quartic):
    return n + 0.5 - 15.0 / 4.0 * cubic **2 * (n ** 2 + n + 11.0 / 30.0) \
         + 3.0 / 2.0 * quartic * (n ** 2 + n + 1.0 / 2.0)

# Partition function using perturbation
def Z_pert(cubic, quartic, beta, n_max):
    Z = sum(math.exp(-beta * Energy_pert(n, cubic, quartic)) for n in range(n_max + 1))
    return Z

# Anharmonic potential
def V(x, cubic, quartic):
    return x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4

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

n_max = 10
quartic_list = [0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5]

print('quartic |     Z    |   Zp')

for quartic in quartic_list:
    cubic = -quartic
    beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
    beta     = 2.0 ** 1                      # actual value of beta (power of 2)
    rho = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
    while beta_tmp < beta:
        rho = numpy.dot(rho, rho)
        rho *= dx
        beta_tmp *= 2.0
    Z = sum(rho[j, j] for j in range(nx + 1)) * dx
    Z_p = Z_pert(cubic, quartic, beta, n_max)
    print('  %.3f | %f | %f'%(quartic, Z, Z_p))

# graphics output
#pylab.title('$\\beta = 2^{%i}$' % math.log(beta, 2))
#pylab.xlabel('$x$', fontsize=18)
#pylab.ylabel('$x\'$', fontsize=18)
#pylab.savefig('plot-anharmonic-rho.png')
#pylab.show()
