import math, numpy, pylab

def pi_quant(x, beta):
    return math.sqrt(math.tanh(beta/2)/math.pi)*math.exp(-x**2*math.tanh(beta/2))

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * 0.5 * (x ** 2 + xp ** 2)) \
                         for x in grid] for xp in grid])

x_max = 5.0
nx = 200
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-(nx - 1) // 2, nx // 2 + 1)] 
beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
beta     = 2.0 ** 2                      # actual value of beta (power of 2)
rho = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
while beta_tmp < beta:
    rho = numpy.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0

# save results
Z = sum(rho[j, j] for j in range(nx + 1)) * dx
pi_of_x = [rho[j, j] / Z for j in range(nx + 1)]
f = open('data_harm_matrixsquaring_beta' + str(beta) + '.dat', 'w')
for j in range(nx + 1):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()

pi_q = [pi_quant(x_i, beta) for x_i in x]

# graphics output
pylab.title('$\\beta = 2^{%i}$' % math.log(beta, 2))
pylab.plot(x, pi_of_x, label='matrix-square')
pylab.plot(x, pi_q, '--', label='analytic')
pylab.xlabel('$x$', fontsize=12)
pylab.ylabel('$\pi(x)$', fontsize=12)
pylab.legend()
pylab.savefig('plot-harmonic-pi.png')
pylab.show()