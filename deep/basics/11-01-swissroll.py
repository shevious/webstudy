# Swiss roll visualization:
from sklearn.datasets import make_swiss_roll
from matplotlib import pyplot as plt
X, t = make_swiss_roll(n_samples=1000, noise=0.2, random_state=42)
#X, t = make_swiss_roll(n_samples=1000, noise=2.0, random_state=42)

axes = [-11.5, 14, -2, 23, -12, 15]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

#ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap=plt.cm.hot)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap='rainbow')
ax.view_init(10, -70)
ax.set_xlabel("$x_1$", fontsize=16)
ax.set_ylabel("$x_2$", fontsize=16)
ax.set_zlabel("$x_3$", fontsize=16)
ax.set_xlim(axes[0:2])
ax.set_ylim(axes[2:4])
ax.set_zlim(axes[4:6])

#save_fig("swiss_roll_plot")
plt.show()


# "squashed" swiss roll visualization:
plt.figure(figsize=(11, 4))

plt.subplot(121)
#plt.scatter(X[:, 0], X[:, 1], c=t, cmap=plt.cm.hot)
plt.scatter(X[:, 0], X[:, 1], c=t, cmap='rainbow')
plt.axis(axes[:4])
plt.xlabel("$x_1$", fontsize=18)
plt.ylabel("$x_2$", fontsize=18, rotation=0)
plt.grid(True)

plt.subplot(122)
plt.scatter(t, X[:, 1], c=t, cmap='rainbow')
plt.axis([4, 15, axes[2], axes[3]])
plt.xlabel("$z_1$", fontsize=18)
plt.grid(True)

#save_fig("squished_swiss_roll_plot")
plt.show()

# "squashed" swiss roll visualization:
plt.figure(figsize=(5, 5))

plt.subplot(111)
plt.scatter(t, X[:, 1], c=t, cmap='rainbow')
plt.axis([4, 15, axes[2], axes[3]])
plt.xlabel("$z_1$", fontsize=16)
plt.ylabel("$z_2$", fontsize=16, rotation=0)
plt.grid(True)

#save_fig("squished_swiss_roll_plot")
plt.show()

X, t = make_swiss_roll(n_samples=1000, noise=2.0, random_state=42)

axes = [-11.5, 14, -2, 23, -12, 15]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

#ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap=plt.cm.hot)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap='rainbow')
ax.view_init(10, -70)
ax.set_xlabel("$x_1$", fontsize=16)
ax.set_ylabel("$x_2$", fontsize=16)
ax.set_zlabel("$x_3$", fontsize=16)
ax.set_xlim(axes[0:2])
ax.set_ylim(axes[2:4])
ax.set_zlim(axes[4:6])

#save_fig("swiss_roll_plot")
plt.show()
