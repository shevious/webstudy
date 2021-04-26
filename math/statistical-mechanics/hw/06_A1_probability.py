import random, math, pylab

def gauss_cut():
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= 1.0:
            return x

# mean = 0, sigma = 1
def gauss_2d(x, y):
    return math.exp(-0.5 * (x**2 + y**2)) / (2*math.pi)

alpha = 0.5
nsamples = 1000000
samples_x = []
samples_y = []

for sample in range(nsamples):
    while True:
        # gaussian sampling
        x = gauss_cut()
        y = gauss_cut()
        #p = math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4)) / (gauss_2d(x, y) / gauss_2d(0, 0))
        p = math.exp(-alpha * (x ** 4 + y ** 4))
        if random.uniform(0.0, 1.0) < p:
            break
    samples_x.append(x)
    samples_y.append(y)

pylab.figure(figsize=(6,10))
pylab.subplot(2, 1, 1)
pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A1_1 gaussian')

samples_x = []
samples_y = []

for sample in range(nsamples):
    while True:
        # uniform sampling
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        p = math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4)) 
        if random.uniform(0.0, 1.0) < p:
            break
    samples_x.append(x)
    samples_y.append(y)

pylab.subplot(2, 1, 2)
pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A1_1 uniform')
pylab.savefig('plot_A1_1.png')
pylab.show()
