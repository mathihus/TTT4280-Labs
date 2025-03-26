import numpy as np

with open("more_angle_estimates_tuned.csv", "r") as file:
    stds = []
    for row in file:
        row = row.split(";")
        row = [float(i) for i in row]

        stds.append(np.std(row, ddof=1))

        print(row)

print(stds)
print(np.array(stds)**2)

