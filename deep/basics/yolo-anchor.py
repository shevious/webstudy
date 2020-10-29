import numpy as np
from matplotlib import pyplot as plt

anchors = np.array([12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401])
anchors = anchors.reshape((9,2))
from matplotlib.patches import Rectangle

anchors = anchors
plt.figure()
ax = plt.gca()
ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
for i in range(9):
  if i in range(0,3):
    color = 'blue'
  elif i in range(3,6):
    color = 'green'
  else:
    color = 'red'
  ax.add_patch(Rectangle((-anchors[i][0], -anchors[i][1]), 2*anchors[i][0], 2*anchors[i][1], fill=None, alpha=1, edgecolor=color))
  #print(anchors[i,0], anchors[i,1])
plt.show()

'''
someX, someY = 0.5, 0.5
plt.figure()
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, fill=None, alpha=1))
plt.show()
'''
