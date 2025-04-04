from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np

def lag(signal1, signal2, mic):
    corr = np.correlate(signal1, signal2, "full")

    lag_n = len(signal1)
    x = np.arange(lag_n-50, lag_n+50)
    interpcorr = np.interp(x, np.arange(len(corr)), corr)

    lag_estimate = (np.argmax(interpcorr))-len(x)//2+1

    plt.plot(x, interpcorr, label=mic)
    return -lag_estimate

def angle(signal1, signal2, signal3, plot=False):
    n21 = lag(signal2, signal1, r"$n_{21}$")
    n31 = lag(signal3, signal1, r"$n_{31}$")
    n32 = lag(signal3, signal2, r"$n_{32}$")

    print(f"n21 = {n21}, n31 = {n31}, n32 = {n32}")

    if plot:
        plt.legend()
        plt.show()

    angle_estimate = -np.arctan(np.sqrt(3)*((n31+n21)/(n31-n21+2*n32)))

    if (n31-n21+2*n32) < 0:
        angle_estimate += np.pi
    if angle_estimate > 1.1*np.pi:
        angle_estimate -= 2*np.pi

    return angle_estimate

def angle_detect(deg, i, plot=False):
    sample_period, data = raspi_import(f'data/{deg}/{deg}_deg_{i}.bin') # converting binary file to array with raspi_import.py

    data -= (2**12-1)/2 # subtracting offset
    data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt for plotting of time signal

    skip_samples = 3000 # skipping the first x samples to get rid off noise at the start of sampling
    end_samples = len(data[:, 0])-10000

    signal1, signal2, signal3 = data[skip_samples:end_samples, 2], data[skip_samples:end_samples, 0], data[skip_samples:end_samples, 1]

    if plot:
        fig, ax = plt.subplots(3, 1) # setting up figure to put subplots of time series
        fig.tight_layout(pad=0.5)

        time = np.arange(len(signal1))*sample_period

        for i in range(3): # Plotting data channel i
            ax[i].plot(time, data[skip_samples:end_samples, i])
            ax[i].set_title(f"Mikrofon {i+1}:")
            ax[i].set_ylim(-2, 2)
            ax[i].set_ylabel("Amplitude [V]")
            ax[i].set_xlabel("Tid [s]")
        plt.show()

    angle_estimate = angle(signal1, signal2, signal3, plot)
    
    return (angle_estimate*180/np.pi) # taking absolute angle and converitng to degrees from rad


def create_angle_matrix():

    angles = np.zeros((8, 5))

    for i in range(8):
        for n in range(5):
            a = angle_detect(45*i, n+1)
            angles[i, n] = a

    np.savetxt("angle_estimates_matrix.csv", angles, delimiter=";")
    return angles

def lag_to_angle(lag1, lag2, lag3):
    
    angle_estimate = -np.arctan(np.sqrt(3)*((lag2+lag1)/(lag2-lag1+2*lag3)))

    if (lag2-lag1+2*lag3) < 0:
        angle_estimate += np.pi
    if angle_estimate > 1.1*np.pi:
        angle_estimate -= 2*np.pi

    return angle_estimate*180/np.pi

def all_possible_lags(max_lags):
    angles = []
    
    for i in range(-max_lags, max_lags+1):
        for n in range(-max_lags, max_lags+1):
            for k in range(-max_lags, max_lags+1):
                a = lag_to_angle(i, n, k)
                angles.append(a)
                # print(i, n, k, ":", a)
    
    return set(angles)


def create_angle_matrix_2():
    d = 2

    angles = np.zeros((8, d*5))

    for i in range(8):
        for n in range(0, d*5, d):
            a = angle_detect(45*i, n//d+1)
            for k in range(d):
                angles[i, n+k] = a

    np.savetxt("more_angle_estimates.csv", angles, delimiter=";")
    return angles


angles = all_possible_lags(3)
print(angles)


# create_angle_matrix_2()

print(angle_detect(90, 5))#, True)

# for i in range(8):
#     print(f"Actual angle: {45*i} - Meassured angle: {angle_detect(45*i, 2)} \n")

