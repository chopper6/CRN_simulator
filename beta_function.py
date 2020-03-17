from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import scipy.special as sc
import matplotlib.pyplot as plt
import numpy as np

k = 3
I = lambda x: sc.betainc(k*x, x, k/(k+1))
P = lambda X: sc.betainc(X[0], X[1], k/(k+1)) / I(1)

# where Prob( ... = 3/4 | X[0], X[1] ) <= P

def getP(mx, my):
    output = np.zeros_like(mx)
    for i, mxi in enumerate(mx.flat):
        myi = list(my.flat)[i]
        output.flat[i] = P( [mxi, myi] )
    return output

x = range(10)
y = [I(t) for t in x]

plt.plot(x, y)
plt.show()


x = np.arange(1, 40, 1.0)
y = np.arange(1, 40, 1.0)
x, y = np.meshgrid(x, y)
z = getP(x,y)

print(z)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True)

plt.show()