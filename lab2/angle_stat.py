import numpy as np
import matplotlib.pyplot as plt

def std(T):
    s = 0

    n = len(T)
    print(n)

    for t in T:
        s += ((t-np.mean(T))**2) / (n-1)

    s = np.sqrt(s)
    return s


with open("more_angle_estimates_tuned.csv", "r") as file:
    stds = []
    stds2 = []
    means = []

    for row in file:
        row = row.split(";")
        row = [float(i) for i in row]

        stds.append(np.std(row, ddof=1))
        # stds2.append(std(row))
        means.append(np.mean(row))

    vars = np.array(stds)**2

# print(np.array(stds)-np.array(stds2))

n = 10
tp = 2.262 # t value for n = 10-1 = 9 samples

confidence_intervals = []

for i in range(len(stds)):
    confidence_intervals.append((means[i]-tp*(stds[i]/np.sqrt(n)), means[i]+tp*(stds[i]/np.sqrt(n))))
    print(45*i, tp*(stds[i]/np.sqrt(n)))

print(confidence_intervals)

x = [i*45 for i in range(-3, 5)]

plt.plot(x, x)

with open("more_angle_estimates_tuned.csv", "r") as file:
    l = 0
    for row in file:
        row = row.split(";")
        row = [float(i) for i in row]

        deg = x[l-5]
        plt.scatter(np.zeros(10)+deg, row, s=100, facecolors='none', edgecolors="black")
        plt.plot([deg, deg], confidence_intervals[l], linewidth=5)#, solid_capstyle="butt")

        l += 1

plt.xlim(-140, 185)
plt.show()