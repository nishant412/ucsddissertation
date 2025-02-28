import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.loglog(range(1, 360, 5), range(1, 360, 5))
ax.set_xlabel('frequency [Hz]')

def invert(x):
    # 1/x with special treatment of x == 0
    x = np.array(x).astype(float)
    near_zero = np.isclose(x, 0)
    x[near_zero] = np.inf
    x[~near_zero] = 1 / x[~near_zero]
    return x

# the inverse of 1/x is itself
secax = ax.secondary_xaxis(0.0, functions=(invert, invert))
secax.spines["bottom"].set_position(("axes",-0.3))
secax.set_xlabel('Period [s]')
plt.show()
