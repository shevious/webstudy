
import matplotlib.pyplot as plt
import numpy as np

# 100 linearly spaced numbers
x = np.linspace(1,50,100)

# the function, which is y = x^2 here
alpha = 1.16 # 8:2
alpha = 1.42096 # 7:3 y = x**(-alpha)

'''
# setting the axes at the centre
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# plot the function
plt.plot(x,y, 'r')

# show the plot
plt.show()
'''

N = 1000

max_salary = 30

x = np.linspace(1,max_salary,max_salary)
#print(x)

#n_x = alpha*(x**(-alpha-1))
n_x = x**(-alpha) - (x+1)**(-alpha)
N_x = n_x*N
#print(N_x)
N_x = np.trunc(N_x)
#print(N_x)

sum = 0
for i in range(0, max_salary, 1):
  sum += N_x[i]

#print(sum)
I = 1000000.
A = alpha/(alpha-1)
print('A = ', A)

n = np.linspace(1,N,N)
#print(n)
x = (n/N)**((alpha-1)/alpha) - ((n-1)/N)**((alpha-1)/alpha)
x = np.trunc(I*x)
print(x)

sum = 0
N_p = int(N*9/100)
for i in range(0, N_p, 1):
  sum += x[i]
print(sum)

# setting the axes at the centre
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# plot the function
plt.plot(n,x, 'r')

# show the plot
plt.show()
