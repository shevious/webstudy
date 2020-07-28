n = 100

a = []
av1 = []
av2 = []
av3 = []

for i in range(0, n, 1):
  if (i%2 == 0):
    mul = -1
  else:
    mul = 1
  a.append(mul*i*i)
  sum = 0
  for j in range(0, i+1, 1):
    sum += a[j]
  av1.append(sum)

  sum = 0
  for j in range(0, i+1, 1):
    sum += av1[j]
  av2.append(sum)

  sum = 0
  for j in range(0, i+1, 1):
    sum += av2[j]
  av3.append(sum)

for i in range(0, n, 1):
  av1[i] = av1[i]/(i+1)
  av2[i] = av2[i]/(i+1)**2
  av3[i] = av3[i]/(i+1)**3

print(av1)
print(av2)
print(av3)
    
