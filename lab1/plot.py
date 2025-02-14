from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('1k.bin') # converting binary file to array with raspi_import.py

data -= (2**12-1)/2 #+16.5 # subtracting offset
data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt

data_length = data.shape[0] # getting the length of samples
data_channels = data.shape[1] # getting amount of channels

n = np.arange(data_length) # making a list with same length as data to be the x-axis of plotting later
time = n*(sample_period) # scaling x-axis to time in seconds

w = np.sin(np.pi*n/ data_length)**2 # hanning window function

fig, ax = plt.subplots(data_channels, 1) # setting up figure to put subplots of time series
fig.tight_layout(pad=0.5)

for i in range(data_channels): # Plotting data channel i
    ax[i].plot(time, data[:, i])
    ax[i].set_title(f"ADC {i+1}:")
    ax[i].set_xlim(0, 0.05)
    ax[i].set_ylim(-2, 2)
    ax[i].set_ylabel("Amplitude [V]")
    ax[i].set_xlabel("Tid [s]")
plt.show()

N = 2**15 # setting FFT length to closest 2 power of data_length
# N = data_length

Sdb = np.zeros((N, data_channels)) # making empty array to put fft values into

fs = int(1/sample_period) # samplings frequency
df = np.linspace(-0.5, 0.5, N)*fs # making scaled frequency axis

fig1, ax1 = plt.subplots(data_channels, 1) # setting up figure to put subplots of PDS
fig1.tight_layout(pad=0.5)

for i in range(data_channels):
    data[:, i] = w*data[:, i] # using hanning window on channel i

    fft = abs(np.fft.fft(data[:, i], N)) # reshaping data to be an 1d array and taking fft
    fft = abs(np.fft.fftshift(fft)) # shifting spectrum and taking absolute value 

    Sdb[:, i] = 20*np.log10(fft/max(fft)) # db scale and normalising of fft

    ax1[i].plot(df, Sdb[:, i])
    ax1[i].set_title(f"ADC {i+1}:")
    ax1[i].set_xlim(10, 15000)
    ax1[i].set_ylim(-120,)
    ax1[i].set_ylabel("Effekt [dB]")
    ax1[i].set_xlabel("Frekvens [Hz]")
    ax1[i].set_xscale("log")
plt.show()

for i in range(data_channels):
    f = np.argmax(Sdb[int(N/2):, i]) # finding the frequency of the signal. Only works with no zero-padding, else enter it manually.
    # f = 1000
    print(f"f = {f}Hz")
    B = f/10 # defining the bandwidth of the desired frequency for SNR calculations

    # signal_power = np.mean(Sdb[int((N)*(sample_period*(f-(B/2)) + 1/2)):int((N)*(sample_period*(f+(B/2)) + 1/2)), i])
    signal_power = 0 # because of the normalisation of PDS

    # taking the max value from the PDS from 10 -> f-(B/2) and f+(B/2) -> inf
    noise_power_harmonic = max(max(Sdb[int(N/2)+10:int((N)*(sample_period*(f-(B/2)) + 1/2)), i]), max(Sdb[int((N)*(sample_period*(f+(B/2)) + 1/2)):, i]))

    # taking the max value from the PDS from 10 -> f-(B/2) and f+(B/2) -> 2*f-(B/2). Only looking to 2*f-(B/2) to neglect the harmonic frequencies.
    noise_power = max(max(Sdb[int(N/2)+10:int((N)*(sample_period*(f-(B/2)) + 1/2)), i]), max(Sdb[int((N)*(sample_period*(f+(B/2)) + 1/2)):int((N)*(sample_period*(2*f-(B/2)) + 1/2)), i]))

    print("SNR includic harmonic noise", signal_power-noise_power_harmonic)
    print("SNR excluding harmonic noise", signal_power-noise_power)

print("Theoretical SNR max =", 20*np.log10((np.sqrt(6)/2)*(2**12)*(3.3/3.3)))



    
