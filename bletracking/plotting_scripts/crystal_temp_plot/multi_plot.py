import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6, 4))

ax1 = fig.add_axes([0.1, 0.1, 0.25, 0.25])
ax2 = fig.add_axes([0.1, 0.2, 0.85, 0.75])
#ax3 = fig.add_axes([0.6, 0.2, 0.2, 0.65])

#ax1.text(0.01, 0.95, "ax1", size=12)
#ax2.text(0.05, 0.8, "ax2", size=12)
#ax3.text(0.05, 0.9, "ax3", size=12)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.spines["top"].set_visible(False)
ax1.set_yticks([])

plt.show()
