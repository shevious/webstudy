import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D

#Parameters to set
mu_x = 0
variance_x = 3

mu_y = 0
variance_y = 15

#Create grid and multivariate normal
x = np.linspace(-10,10,500)
y = np.linspace(-10,10,500)
X, Y = np.meshgrid(x,y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X; pos[:, :, 1] = Y
rv = multivariate_normal([mu_x, mu_y], [[variance_x, 0], [0, variance_y]])

#Make a 3D plot
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, rv.pdf(pos),cmap='viridis',linewidth=0)
ax.plot_surface(X, Y, rv.pdf(pos),cmap='rainbow',linewidth=0)
#ax.scatter(0,0,0, color='red')
#ax.set_xlabel('X axis')
#ax.set_ylabel('Y axis')
#ax.set_zlabel('Z axis')
ax.set_xlabel('$z_1$')
ax.set_ylabel('$z_2$')
#ax.set_zlabel('Z axis')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
#ax.set_zlim(0, 1)
plt.show()


#Create grid and multivariate normal
x = np.linspace(-10,10,500)
y = np.linspace(-10,10,500)
X, Y = np.meshgrid(x,y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X; pos[:, :, 1] = Y
rv = multivariate_normal([mu_x, mu_y], [[variance_x, 0], [0, variance_y]])

#Make a 3D plot
fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.plot_surface(X, Y, rv.pdf(pos),cmap='viridis',linewidth=0)
#ax.plot_surface(X, Y, rv.pdf(pos),cmap='rainbow',linewidth=0)
ax.scatter(0,0,0, color='red')
#ax.set_xlabel('X axis')
#ax.set_ylabel('Y axis')
#ax.set_zlabel('Z axis')
ax.set_xlabel('$z_1$')
ax.set_ylabel('$z_2$')
#ax.set_zlabel('Z axis')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
ax.set_zlim(0, 1)
plt.show()

