import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


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
        # tp = 4.604

        confidence_intervals = []

        for i in range(len(stds)):
            confidence_intervals.append((means[i]-tp*(stds[i]/np.sqrt(n)), means[i]+tp*(stds[i]/np.sqrt(n))))
            # print(45*i, tp*(stds[i]/np.sqrt(n)))

        print([(round(number[0], 2), round(number[1], 2)) for number in confidence_intervals])

        print(means)
        print(stds)

        return confidence_intervals


def confidence_plot(filename, confidence_intervals):
    x = [i*45 for i in range(-3, 5)]

    plt.plot(x, x, color="black")#, linestyle=":")

    with open(filename, "r") as file:
        l = 0
        for row in file:
            row = row.split(";")
            row = [float(i) for i in row]

            deg = x[l-5]

            label = [0, 45, 90, 135, 180, -135, -90, -45]

            # plt.scatter(label[l], label[l], edgecolors="black", facecolors="none")
            
            plt.plot([deg, deg], confidence_intervals[l], linewidth=5, label=label[l], solid_capstyle="butt")
            # plt.scatter(np.zeros(5)+deg, row, s=50, label=label[l])#, edgecolors="black", facecolor="none")

            l += 1


    plt.xlim(-140, 185)
    plt.legend()
    plt.xlabel("Vinkel til lydkilde [grader]")
    plt.xlim(-140, 190)
    plt.ylabel("Estimert vinkel [grader]")
    # plt.title("95% konfidensintervall uten interpolasjon")
    # plt.title("Vinkelestimat mot teroetisk vinkel uten interpolasjon")
    plt.title("95% konfidensintervall med 8x interpolasjon")
    # plt.title("Vinkelestimat mot teroetisk vinkel med 8x interpolasjon")

    ax = plt.gca()

    ax.xaxis.set_major_locator(MultipleLocator(45))   # x-axis step = 2
    ax.yaxis.set_major_locator(MultipleLocator(45))  # y-axis step = 10

    plt.show()


def table(filename):
    with open(filename, "r") as file:

        for row in file:
            row = row.split(";")
            row = [round(float(i), 2) for i in row]
            row = str(row)
            row = row.replace(",", " &").replace("[", "").replace("]", "")
            print(row)

confidence_interval("angle_estimates_matrix_1_1.csv")
# confidence_interval("angle_estimates_matrix_4.csv")
confidence_interval("angle_estimates_matrix_8_1.csv")
# confidence_interval("angle_estimates_matrix_12.csv")

# confidence_plot("angle_estimates_matrix_1.csv", confidence_interval("angle_estimates_matrix_1.csv"))
# confidence_plot("angle_estimates_matrix_4.csv")
# confidence_plot("angle_estimates_matrix_8.csv", confidence_interval("angle_estimates_matrix_8.csv"))
# confidence_plot("angle_estimates_matrix_12.csv")

# table("angle_estimates_matrix_8.csv")