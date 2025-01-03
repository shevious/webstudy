import random
import math
import pylab
import os

#eta = 0.3
#N = 4
#eta = 0.72
#N = 64
eta = 0.42
N = 64
sigma = math.sqrt(eta/(N*math.pi))
delta = 0.3*sigma
#n_steps = 1000
#n_steps = 10000
n_steps = 0
filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  math.sqrt(d_x**2 + d_y**2)

def show_conf(L, sigma, title, fname):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()

def read_or_create_config(N, eta, create=False):
    if os.path.isfile(filename) and not create:
        f = open(filename, 'r')
        L = []
        for line in f:
            a, b = line.split()
            L.append([float(a), float(b)])
        f.close()
        print('starting from file', filename)
    else:
        N_sqrt = int(math.sqrt(N))
        delxy = 1./(2.*N_sqrt)
        two_delxy = 2.*delxy

        L = [[delxy + i * two_delxy, delxy + j * two_delxy] for i in range(N_sqrt) for j in range(N_sqrt)]

        print('starting from a new configuration')

    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        # periodic boundary condition
        b[0] = b[0] % 1.0
        b[1] = b[1] % 1.0
        min_dist = min(dist(b,c) for c in L if c != a)
        if not (min_dist < 2.0 * sigma):
            a[:] = b

    return L

L = read_or_create_config(N, eta, False)

f = open(filename, 'w')
for a in L:
   f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
f.close()

#print(L)

show_conf(L, sigma, 'test graph', 'disks.png')
