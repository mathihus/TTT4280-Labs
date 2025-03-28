import numpy as np

with open("more_angle_estimates_tuned.csv", "r") as file:
    stds = []
    means = []

    for row in file:
        row = row.split(";")
        row = [float(i) for i in row]

        stds.append(np.std(row, ddof=1))
        means.append(np.mean(row))

    vars = np.array(stds)**2

print(stds)
print(vars)

n = 10
tp = 2.228 # t value for n = 10 samples

confidence_intervals = []

for i in range(len(stds)):
    confidence_intervals.append((means[i]-tp*(stds[i]/np.sqrt(n)), means[i]+tp*(stds[i]/np.sqrt(n))))
    print(45*i)

print(confidence_intervals)