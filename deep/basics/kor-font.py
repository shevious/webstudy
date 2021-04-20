import matplotlib.pyplot as plt
import numpy as np
import matplotlib

import matplotlib.font_manager as fm  
font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
#fontprop = fm.FontProperties(fname=font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
matplotlib.rc('font', family=font_name)

x = np.linspace(-3,7,100)
plt.plot(x, 0.5*x+1)
plt.plot(x, 0.5*x+2)
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
#plt.legend(['가나다', 'Test'], loc='upper left')
plt.legend(['가나다', 'Test'], loc='upper left', prop={'family':font_name, 'size':20})
plt.show()

import glob

mylist = [f for f in glob.glob("*.txt")]
print(mylist)

x = np.linspace(-3,7,100)
plt.plot(x, 0.5*x+1)
plt.plot(x, 0.5*x+2)
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(mylist, loc='upper left', prop={'family':font_name, 'size':20})
plt.show()

import os

arr = os.listdir()
#print(arr)

folder = './'
f = []
for (dirpath, dirnames, filenames)  in os.walk(folder):
  f.extend(filenames)
  break
print(filenames)
tt = []
for ff in filenames:
  tt.append(os.path.splitext(ff)[0])
print(tt)

txt = []
for file_name in filenames:
  if '.txt' in file_name:
    txt.append(file_name)

print(txt)

x = np.linspace(-3,7,100)
#plt.plot(x, 0.5*x+1, label=filenames[7])
#plt.plot(x, 0.5*x+2, label=filenames[0])
plt.plot(x, 0.5*x+1, label=filenames[7])
plt.plot(x, 0.5*x+2, label=tt[0])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
#plt.legend(txt, loc='upper left', prop={'family':font_name, 'size':20})
plt.legend()
plt.show()
