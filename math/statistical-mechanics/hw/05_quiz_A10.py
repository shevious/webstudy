import random, math

sigma = 0.2
for t in range(1000):
    L = [(random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))]
    while True:
        a = (random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))
        min_dist = min(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for b in L)
        if min_dist > 2.0 * sigma:
            L.append(a)
            if len(L) == 4: break
    print(L)

'''
Correct:
Program 
A10 is a valid algorithm for random sequential deposition    for small 
radii sigma where it always terminates in finite time. For larger sigma,
 it is invalid, as it may run forever.

Incorrect:
The legal hard-disk configurations L output by program A10 satisfy the
equiprobability principle.
'''
