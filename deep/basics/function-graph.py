import numpy as np
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm  # 폰트 관련 용도
font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
fontprop = fm.FontProperties(fname=font_path)

x = np.linspace(-3,7,100)
fig, ax = plt.subplots()
ax.plot(x, 0.5*x+1)
ax.set_aspect('equal')
ax.grid(True, which='both')
# set the x-spine (see below for more info on `set_position`)
ax.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax.spines['right'].set_color('none')
ax.yaxis.tick_left()

# set the y-spine
ax.spines['bottom'].set_position('zero')
# turn off the top spine/ticks
ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()
plt.title('가나다', fontproperties=fontprop)
plt.show()

x = np.linspace(0.2,10,100)
fig, ax = plt.subplots()
ax.plot(x, 1/x)
ax.plot(x, np.log(x))
ax.set_aspect('equal')
ax.grid(True, which='both')

# set the x-spine (see below for more info on `set_position`)
ax.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax.spines['right'].set_color('none')
ax.yaxis.tick_left()

# set the y-spine
ax.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()
plt.show()
