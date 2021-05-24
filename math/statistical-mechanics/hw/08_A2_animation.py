import random, math, os, pylab
from matplotlib import animation
import numpy as np

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

L = 128
#L = 32
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}

#T = 3.0
T = 2.27
#T = 1.0

#S = [random.choice([1, -1]) for k in range(N)]
filename = 'data_local_'+ str(L) + '_' + str(T) + '.txt'
if os.path.isfile(filename):
    f = open(filename, 'r')
    S = []
    for line in f:
        S.append(int(line))
    f.close()
    print('Starting from file', filename)
else:
    S = [random.choice([1, -1]) for k in range(N)]
    print('Starting from a random configuration')
    
def x_y(k, L):
    y = k // L
    x = k - y * L
    return x, y

conf = [[0 for x in range(L)] for y in range(L)]
for k in range(N):
    x, y = x_y(k, L)
    conf[x][y] = S[k]
    
fig = pylab.figure()
ax = pylab.axes()
im = pylab.imshow(conf, extent=[0, L, 0, L], interpolation='nearest')
pylab.set_cmap('hot')
pylab.title('Local_'+ str(T) + '_' + str(L))
ttl = ax.text(.5, 1.05, '', color='red', bbox=dict(facecolor='gray', alpha=0.5))

def init():
    im.set_data(conf)
    return im

nsteps = N * 10000
nskip = 10000
#nsteps = 300
beta = 1.0 / T
Energy = energy(S, N, nbr)
E = []

def animate(step):
    global Energy, S, E
    for i in range(nskip):
        k = random.randint(0, N - 1)
        delta_E = 2.0 * S[k] * sum(S[nn] for nn in nbr[k])
        if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
            S[k] *= -1
            Energy += delta_E
        E.append(Energy)
    for k in range(N):
        x, y = x_y(k, L)
        conf[x][y] = S[k]
    im.set_array(conf)
    title_text = 'nsteps = %i'%(step*nskip)
    ttl.set_text(title_text)
    return [im, ttl]

#for step in range(nsteps):
#    k = random.randint(0, N - 1)
#    delta_E = 2.0 * S[k] * sum(S[nn] for nn in nbr[k])
#    if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
#        S[k] *= -1
#        Energy += delta_E
#    E.append(Energy)
#print('mean energy per spin:', sum(E) / float(len(E) * N))

anim = animation.FuncAnimation(fig, animate, 
                               frames=nsteps, 
                               interval=1,
                               blit=True)


f = open(filename, 'w')
for a in S:
   f.write(str(a) + '\n')
f.close()



#pylab.savefig('plot_A2_local_'+ str(T) + '_' + str(L)+ '.png')
pylab.show()
