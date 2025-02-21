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
    n21 = lag(signal2, signal1, "n21")
    n31 = lag(signal3, signal1, "n31")
    n32 = lag(signal3, signal2, "n32")

    if plot:
        plt.legend()
        plt.show()

    angle_estimate = -np.arctan(np.sqrt(3)*((n31+n21)/(n31-n21+2*n32)))

    if (n31-n21+2*n32) < 0:
        angle_estimate += np.pi
    elif angle_estimate < 0:
        angle_estimate += 2*np.pi

    return angle_estimate

def angle_detect(deg, i, plot=False):
    sample_period, data = raspi_import(f'data/{deg}/{deg}_deg_{i}.bin') # converting binary file to array with raspi_import.py

    data -= (2**12-1)/2 # subtracting offset
    data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt for plotting of time signal

    skip_samples = 3000 # skipping the first x samples to get rid off noise at the start of sampling

    signal1, signal2, signal3 = data[skip_samples:, 2], data[skip_samples:, 0], data[skip_samples:, 1]

    if plot:
        fig, ax = plt.subplots(3, 1) # setting up figure to put subplots of time series
        fig.tight_layout(pad=0.5)

        time = np.arange(len(signal1))*sample_period

        for i in range(3): # Plotting data channel i
            ax[i].plot(time, data[skip_samples:, i])
            ax[i].set_title(f"Microphone {i+1}:")
            ax[i].set_ylim(-2, 2)
            ax[i].set_ylabel("Amplitude [V]")
            ax[i].set_xlabel("Tid [s]")
        plt.show()

    angle_estimate = angle(signal1, signal2, signal3, plot)
    
    return abs(angle_estimate*180/np.pi) # taking absolute angle and converitng to degrees from rad

for i in range(8):
    print(45*i, "-", angle_detect(45*i, 2))



