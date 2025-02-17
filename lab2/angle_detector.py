from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np
import math as m

sample_period, data = raspi_import('out-2025-02-17-11.16.35.bin') # converting binary file to array with raspi_import.py

data -= (2**12-1)/2 #+16.5 # subtracting offset
data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt

skip_samples = 3000

data_length = data.shape[0]-skip_samples # getting the length of samples
data_channels = 3 # getting amount of channels

signal1, signal2, signal3 = data[skip_samples:, 2], data[skip_samples:, 0], data[skip_samples:, 1]

# max_lag = 6
# n_lag = 5
# signal2 = data[skip_samples:-n_lag, 0]
# signal1 = data[skip_samples+n_lag:, 0]
# signal3 = data[skip_samples+n_lag:, 0]

# def lag(signal1, signal2):
#     cross_corr = np.zeros(2*max_lag+1)

#     for i in range(len(cross_corr)):
#         cross_corr[i] = np.correlate(signal1[i:-len(cross_corr)+i], signal2[:-len(cross_corr)])        
#         # print(np.correlate(signal1[i:len(signal1)-len(cross_corr)+i], signal2[:(len(signal2)-len(cross_corr))]))

#     return -np.argmax(cross_corr) # returning the lag that gives the highes crosscorrolation


n = np.arange(data_length) # making a list with same length as data to be the x-axis of plotting later
time = n*(sample_period) # scaling x-axis to time in seconds

def lag(signal1, signal2):
    corr = np.correlate(signal1, signal2, "full")

    lag_n = data_length
    x = np.arange(lag_n-10, lag_n+10)
    interpcorr = np.interp(x, np.arange(len(corr)), corr)

    print(interpcorr)

    lag_estimate = (np.argmax(interpcorr))-len(x)/2+1
    print(lag_estimate)

    plt.plot(x, interpcorr)
    return lag_estimate

# corr_lag = lag(signal1, signal2, max_lag)
# print(corr_lag, corr_lag*sample_period)

def angle(signal1, signal2, signal3):
    n21 = lag(signal2, signal1)
    n31 = lag(signal3, signal1)
    n32 = lag(signal3, signal2)

    plt.show()

    print(n21, n31, n32)

    angle_estimate = np.arctan(np.sqrt(3)*((n31+n21)/(n31-n21+2*n32)))# - (10/180)*np.pi

    print(angle_estimate*180/np.pi)

    # angle_estimate = np.pi - angle_estimate

    if angle_estimate < 0 or m.copysign(1, angle_estimate) < 0:
        angle_estimate += 2*np.pi

    return angle_estimate

angle_estimate = angle(signal1, signal2, signal3)
print(angle_estimate*180/np.pi)

# fig, ax = plt.subplots(data_channels, 1) # setting up figure to put subplots of time series
# fig.tight_layout(pad=0.5)

# for i in range(data_channels): # Plotting data channel i
#     ax[i].plot(time, data[skip_samples:, i])
#     ax[i].set_title(f"Microphone {i+1}:")
#     # ax[i].set_xlim(0, 0.05)
#     ax[i].set_ylim(-2, 2)
#     ax[i].set_ylabel("Amplitude [V]")
#     ax[i].set_xlabel("Tid [s]")
# plt.show()
