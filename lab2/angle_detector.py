from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('1k.bin') # converting binary file to array with raspi_import.py

data -= (2**12-1)/2 #+16.5 # subtracting offset
data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt

skip_samples = 20

data_length = data.shape[0]-skip_samples # getting the length of samples
data_channels = 3 # getting amount of channels

n = np.arange(data_length) # making a list with same length as data to be the x-axis of plotting later
time = n*(sample_period) # scaling x-axis to time in seconds

lag = 3
max_lag = 6

signal1 = data[skip_samples:data.shape[0]-lag, 0]
signal2 = data[skip_samples+lag:, 0]

def lag(signal1, signal2, max_lag):
    cross_corr = np.zeros(2*max_lag+1)

    for i in range(len(cross_corr)):
        cross_corr[i] = np.correlate(signal1[i:len(signal1)-len(cross_corr)+i], signal2[:(len(signal2)-len(cross_corr))])
        
        # print(np.correlate(signal1[i:len(signal1)-len(cross_corr)+i], signal2[:(len(signal2)-len(cross_corr))]))
    return np.argmax(cross_corr)

print(lag(signal1, signal2, max_lag)*sample_period)


fig, ax = plt.subplots(data_channels, 1) # setting up figure to put subplots of time series
fig.tight_layout(pad=0.5)

for i in range(data_channels): # Plotting data channel i
    ax[i].plot(time, data[skip_samples:, i])
    ax[i].set_title(f"Microphone {i+1}:")
    ax[i].set_xlim(0, 0.05)
    ax[i].set_ylim(-2, 2)
    ax[i].set_ylabel("Amplitude [V]")
    ax[i].set_xlabel("Tid [s]")
plt.show()



    
