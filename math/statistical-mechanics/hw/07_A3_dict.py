import math, random, pylab

def levy_harmonic_path(k):
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

def prob_r_distinguishable(r, beta):
    sigma = math.sqrt(2.0) / math.sqrt(2.0 * math.tanh(beta / 2.0))
    prob = (math.sqrt(2.0 / math.pi) / sigma) * math.exp(- r ** 2 / 2.0 / sigma ** 2)
    return prob

beta = 0.1
nsteps = 1000000
low_1, low_2 = levy_harmonic_path(2)
x = {low_1:low_1, low_2:low_2}
data = []
for step in range(nsteps):
    # move 1
    a = random.choice(list(x.keys()))
    if a == x[a]:
        dummy = x.pop(a)
        a_new = levy_harmonic_path(1)[0]
        x[a_new] = a_new
    else:
        a_new, b_new = levy_harmonic_path(2)
        x = {a_new:b_new, b_new:a_new}
    # move 2
    (low1, high1), (low2, high2) = list(x.items())
    weight_old = rho_harm_1d(low1, high1, beta) * rho_harm_1d(low2, high2, beta)
    weight_new = rho_harm_1d(low1, high2, beta) * rho_harm_1d(low2, high1, beta)
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        x = {low1:high2, low2:high1}
    r = abs(list(x.keys())[1] - list(x.keys())[0])
    data.append(r)

# analytic curve
list_r = [0.1 * a for a in range (0, 101)]
list_p = [prob_r_distinguishable(r, beta) for r in list_r]

pylab.title('Two identical bosons distance\n' +
            'nsteps = %i, $\\beta$ = %.1f'%(nsteps, beta))
pylab.hist(data, bins=150, density=True, label='histogram')
pylab.plot(list_r, list_p, label='distinguishable')
pylab.xlabel('$r$')
pylab.ylabel('Histogram')
pylab.xlim(0, 10)
pylab.legend()
pylab.show()
