import numpy as np
import matplotlib.pyplot as plt


def confidence_interval(filename):

    with open(filename, "r") as file:
        stds = []
        means = []

        for row in file:
            row = row.split(";")
            row = [float(i) for i in row]

            stds.append(np.std(row, ddof=1))
            # stds2.append(std(row))
            means.append(np.mean(row))

        vars = np.array(stds)**2

        # print(np.array(stds)-np.array(stds2))

        # n = 10
        # tp = 2.262 # t value for n = 10-1 = 9 samples

        n = 5
        tp = 2.776

        confidence_intervals = []

        for i in range(len(stds)):
            confidence_intervals.append((means[i]-tp*(stds[i]/np.sqrt(n)), means[i]+tp*(stds[i]/np.sqrt(n))))
            # print(45*i, tp*(stds[i]/np.sqrt(n)))

        print([(round(number[0], 2), round(number[1], 2)) for number in confidence_intervals])

        print(means)
        print(stds)

        return confidence_intervals


def confidence_plot(filename):
    x = [i*45 for i in range(-3, 5)]

    plt.plot(x, x, color="black")

    with open(filename, "r") as file:
        l = 0
        for row in file:
            row = row.split(";")
            row = [float(i) for i in row]

            deg = x[l-5]

            label = [0, 45, 90, 135, 180, -135, -90, -45]
            
            # plt.plot([deg, deg], confidence_intervals[l], linewidth=5, color="black")#, solid_capstyle="butt")
            plt.scatter(np.zeros(5)+deg, row, s=50, label=label[l]) #facecolors='black', ,

            l += 1

    plt.xlim(-140, 185)
    plt.legend()
    plt.xlabel("Vinkel til lydkilde [grader]")
    plt.xlim(-140, 190)
    plt.ylabel("Estimert vinkel [grader]")
    plt.show()

confidence_interval("angle_estimates_matrix_1.csv")
confidence_interval("angle_estimates_matrix_4.csv")
confidence_interval("angle_estimates_matrix_8.csv")
# confidence_interval("angle_estimates_matrix_12.csv")

# confidence_plot("angle_estimates_matrix_1.csv")
# confidence_plot("angle_estimates_matrix_4.csv")
# confidence_plot("angle_estimates_matrix_8.csv")
# confidence_plot("angle_estimates_matrix_12.csv")