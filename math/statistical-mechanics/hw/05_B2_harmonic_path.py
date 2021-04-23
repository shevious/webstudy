import math, random, pylab

def rho_free(x, y, beta):    # free off-diagonal density matrix
    return math.exp(-(x - y) ** 2 / (2.0 * beta)) 

def read_file(filename):
    list_x = []
    list_y = []
    with open(filename) as f:
        for line in f:
            x, y = line.split()
            list_x.append(float(x))
            list_y.append(float(y))
    f.close()
    return list_x, list_y

beta = 4.0
N = 10                                             # number of slices
dtau = beta / N
delta = 1.0                                       # maximum displacement on one slice
n_steps = 1000000                                 # number of Monte Carlo steps
x = [0.0] * N                                     # initial path

step_size = 10                                    # histogram record steps
x_hist = []
step_index = 0

for step in range(n_steps):
    k = random.randint(0, N - 1)                  # random slice
    knext, kprev = (k + 1) % N, (k - 1) % N       # next/previous slices
    x_new = x[k] + random.uniform(-delta, delta)  # new position at slice k
    old_weight  = (rho_free(x[knext], x[k], dtau) *
                   rho_free(x[k], x[kprev], dtau) *
                   math.exp(-0.5 * dtau * x[k] ** 2))
    new_weight  = (rho_free(x[knext], x_new, dtau) *
                   rho_free(x_new, x[kprev], dtau) *
                   math.exp(-0.5 * dtau * x_new ** 2))
    if random.uniform(0.0, 1.0) < new_weight / old_weight:
        x[k] = x_new
    if (step % step_size == 0):
        x_hist.append(x[step_index])
        # for all historgram i = 0,...,N-1
        #for x_i in x:
            #x_hist.append(x_i)
        
filename = 'data_harm_matrixsquaring_beta' + str(beta) + '.dat'
list_x, list_y = read_file(filename)

pylab.title('Quantum Monte Carlo\n' \
    + 'N = %i, n_steps = %i, delta = %.1f, $\\beta$ = %.1f'%(N, n_steps, delta, beta))
pylab.xlim(-2.0, 2.0)
pylab.hist(x_hist, bins=200, density=True, label='histogram')
pylab.plot(list_x, list_y, label='matrix square')
pylab.xlabel('$x$[%i]'%(step_index))
pylab.ylabel('Histogram')
pylab.legend()
pylab.show()
