import math, random, pylab

def levy_harmonic_path(k, beta):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)

def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

def pi_two_bosons(x, beta):
    pi_x_1 = math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta / 2.0))
    pi_x_2 = math.sqrt(math.tanh(beta)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta))
    weight_1 = z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta))
    weight_2 = z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta))
    pi_x = pi_x_1 * weight_1 + pi_x_2 * weight_2
    return pi_x

# distinguishable
def pi_x(x, beta):
    sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
    return math.exp(-x ** 2 / (2.0 * sigma ** 2)) / math.sqrt(2.0 * math.pi) / sigma

def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

list_beta = [(0.1+beta/30.*4.9) for beta in range(0, 31)]
fract_two_cycles = [z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta)) for beta in list_beta]
fract_one_cycle = [z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta)) for beta in list_beta]

nsteps = 5000

prob_one_cycle = []
prob_two_cycles = []

for beta in list_beta:
    low = levy_harmonic_path(2, beta)
    high = low[:]
    data = []
    count_one_cycle = 0
    count_two_cycles = 0
    for step in range(nsteps):
        # move 1
        if low[0] == high[0]:
            k = random.choice([0, 1])
            low[k] = levy_harmonic_path(1, beta)[0]
            high[k] = low[k]
        else:
            low[0], low[1] = levy_harmonic_path(2, beta)
            high[1] = low[0]
            high[0] = low[1]
        data += low[:]
        # move 2
        weight_old = (rho_harm_1d(low[0], high[0], beta) *
                      rho_harm_1d(low[1], high[1], beta))
        weight_new = (rho_harm_1d(low[0], high[1], beta) *
                      rho_harm_1d(low[1], high[0], beta))
        if random.uniform(0.0, 1.0) < weight_new / weight_old:
            high[0], high[1] = high[1], high[0]
        if low[0] == high[0]:
            count_one_cycle += 1
        else:
            count_two_cycles += 1
    prob_one_cycle.append(float(count_one_cycle)/(count_one_cycle+count_two_cycles))
    prob_two_cycles.append(float(count_two_cycles)/(count_one_cycle+count_two_cycles))
    print('beta = ', beta)

# analytic curve
pylab.title('Two identical bosons\n' +
            'nsteps = %i'%(nsteps))
pylab.plot(list_beta, prob_one_cycle, 'o', label='one cycle')
pylab.plot(list_beta, prob_two_cycles, 'o', label='two cycles')
pylab.plot(list_beta, fract_one_cycle, label='one cycle analytic')
pylab.plot(list_beta, fract_two_cycles, label='two cycles analytic')
pylab.xlabel('$\\beta$')
pylab.ylabel('Fractions')
pylab.xlim(0, 5)
pylab.legend()
pylab.show()
