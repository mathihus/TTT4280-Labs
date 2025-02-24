import numpy as np

with open("angle_estimates_matrix.csv", "r") as file:
    stds = []
    for row in file:
        row = row.split(";")
        row = [float(i) for i in row]

        stds.append(np.std(row, ddof=1))

        print(row)

print(stds)
print(np.array(stds)**2)

