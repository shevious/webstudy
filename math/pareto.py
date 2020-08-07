
import matplotlib.pyplot as plt
import numpy as np

# 100 linearly spaced numbers
x = np.linspace(1,50,100)

# the function, which is y = x^2 here
alpha = 1.16 # 8:2
alpha = 1.42 # 7:3
y = x**(-alpha)

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

n = np.linspace(0,1,N)

x = n**alpha
print(x)

sum = 0
for i in range(0,N,1):
  sum += x[i]

A = alpha/(alpha-1.)
#print(A)

#print(sum/N)
