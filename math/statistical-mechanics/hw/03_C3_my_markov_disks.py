import random
import math
import pylab
import os
import cmath

#eta = 0.3
#N = 4
eta = 0.72
N = 64
#eta = 0.42
#N = 64
sigma = math.sqrt(eta/(N*math.pi))
delta = 0.3*sigma
#n_steps = 1000
n_steps = 10000
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

def delx_dely(x, y):
    d_x = (x[0] - y[0]) % 1.0
    if d_x > 0.5: d_x -= 1.0
    d_y = (x[1] - y[1]) % 1.0
    if d_y > 0.5: d_y -= 1.0
    return d_x, d_y

def Psi_6(L, sigma):
    sum_vector = 0j
    for i in range(N):
        vector  = 0j
        n_neighbor = 0
        for j in range(N):
            if dist(L[i], L[j]) < 2.8 * sigma and i != j:
                n_neighbor += 1
                dx, dy = delx_dely(L[j], L[i])
                angle = cmath.phase(complex(dx, dy))
                vector += cmath.exp(6.0j * angle)
        if n_neighbor > 0:
            vector /= n_neighbor
        sum_vector += vector
    return sum_vector / float(N)

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
        if steps % 100 == 0:
            Psi_6_abs = abs(Psi_6(L, sigma))
            Psi_6_list.append(Psi_6_abs)
            #print(Psi_6_abs)

    return L

from statistics import mean

print('Warming up for 10 times.')
for i in range(10):
    Psi_6_list = []
    L = read_or_create_config(N, eta)
    f = open(filename, 'w')
    for a in L:
       f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
    f.close()

print('Starting to calculate Psi_6')
Psi_6_avg = []
eta_list = []
while eta >= 0.02:
    Psi_6_list = []
    L = read_or_create_config(N, eta)

    f = open(filename, 'w')
    for a in L:
       f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
    f.close()

    avg = mean(Psi_6_list)
    Psi_6_avg.append(avg)
    eta_list.append(eta)
    print(eta, avg)

    eta -= 0.02
    sigma = math.sqrt(eta/(N*math.pi))
    delta = 0.3*sigma

#print(L)

#show_conf(L, sigma, 'test graph', 'disks_phi.png')

pylab.figure()
pylab.plot(eta_list, Psi_6_avg)
pylab.xlabel('$\eta$')
pylab.ylabel('avg $|\Psi_6|$')
pylab.show()
