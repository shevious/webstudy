import random, math
n_trials = 400000
n_hits = 0
var = 0.0
sum_Obs = 0.0
sum_Obs2 = 0.0
for iter in range(n_trials):
    x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
    Obs = 0.0
    if x**2 + y**2 < 1.0:
        n_hits += 1
        Obs = 4.0
    var += (Obs - math.pi)**2
    sum_Obs += Obs
    sum_Obs2 += Obs**2

avg_Obs = sum_Obs / n_trials
avg_Obs2 = sum_Obs2 / n_trials
var2 = avg_Obs2 - avg_Obs**2
std = math.sqrt(var2)
print(4.0 * n_hits / float(n_trials), math.sqrt(var / n_trials))
print('<Obs> =', avg_Obs)
print('<Obs^2> =', avg_Obs2)
print('<Obs^2> - <Obs>^2 =', var2)
print('sqrt(<Obs^2> - <Obs>^2) =', std)
