import numpy as np

'''
a = [1,2,3,4,5]
b = [[7,60],[6,70],[8,80],[9,90],[10,100]]
c = list(zip(a,b))
d = zip(*c)
print(list(d)[0])
print(list(d)[1])
'''
a = np.array([1,2,3,4,5])
b = np.array([[7,60],[6,70],[8,80],[9,90],[10,100]])
print(a.shape)
print(b.shape)
print(a)
print(b)
print(type(b))

c = np.column_stack([a,b])
#c = np.array(list(zip(a,b)))
print(c)
print(c.shape)
d = c[c[:,1].argsort()]
print('d=')
print(d)
A = d[:,0:1]
B = d[:,1:3]
print(A)
print(B)
d = np.hsplit(d, (1,3))
print(d)
'''
'''
