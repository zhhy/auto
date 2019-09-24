import matplotlib.pyplot as plt

# data
x = [0, 5, 9, 10, 15]
y = [0, 1, 2, 3, 4]


# trick to get the axes
fig, ax = plt.subplots()

# make ticks and tick labels
xticks = range(min(x),max(x),2)
xticklabels = ['2000-01-0' + str(n) for n in range(1, len(xticks) + 1)]

# plot data
ax.plot(x, y, color='green', linewidth=1, linestyle="-", label=f"delay1")

# set ticks and tick labels
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels, rotation=15)

# show the figure
plt.show()