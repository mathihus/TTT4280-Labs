from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('out-2025-01-20-14.01.07.bin')

data -= (2**12-1)/2 #+16.5 # subtracting offset
data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt

data_length = data.shape[0]
data_channels = data.shape[1]

n = np.arange(data_length)
time = n*(sample_period) #scaling x-axis to time in seconds

w = np.sin(np.pi*n/ data_length)**2 # hanning window function

fig, ax = plt.subplots(data_channels, 1) # making subplots
fig.tight_layout(pad=0.5)

for i in range(data_channels): # Plotting data channel i
    ax[i].plot(time, data[:, i])
    ax[i].set_title(f"Channel {i+1} ADC output:")
    ax[i].set_xlim(0, 0.005)
plt.show()

N = 2**21 # setting FFT length

Sdb = np.zeros((N, data_channels)) # making empty array to put fft values into

fs = int(1/sample_period) # samplings frequency
df = np.linspace(-0.5, 0.5, N)*fs # making scaled frequency axis

fig1, ax1 = plt.subplots(data_channels, 1)
fig1.tight_layout(pad=0.5)

f1k = np.zeros(data_channels) # making array to put peak value at 1kHz in spectrum
f1k_index = int((N)*(sample_period*1000 + 1/2)) # finding 1kHz df index
print((df[f1k_index] + df[f1k_index+1])/2)

for i in range(data_channels): 
    # data[:, i] = w*data[:, i] # using hanning window on channel i

    fft = abs(np.fft.fft(data[:, i], N)) # reshaping data to be an 1d array and taking fft
    fft = abs(np.fft.fftshift(fft)) # shifting spectrum and taking absolute value 

    f1k[i] = (fft[f1k_index] + fft[f1k_index+1])/fs # finding amplitude in volts at 1000Hz

    Sdb[:, i] = 20*np.log10(fft/max(fft)) # db scale and normalising of fft

    ax1[i].plot(df, Sdb[:, i])
    ax1[i].set_title(f"Channel {i+1} power density spectrum:")
    ax1[i].set_xlim(-2000, 2000)
plt.show()

print(f1k)

for i in range(data_channels):
    Ideal_rms = ((f1k[i]**2)/2) #rms squared
    Measured_rms = (1/data_length)*sum(data[:,i]**2) #rms squared
    Noise_rms = (Measured_rms) - (Ideal_rms)
    print("Ideal_rms² =", Ideal_rms)
    print("Measured_rms² =", Measured_rms)
    print("Noise_rms² =", Noise_rms)
    SNR = 10*np.log10(Measured_rms/(Noise_rms))

    print(f"SNR channel {i+1}: {SNR}dB \n")

print("Theoretical SNR max =", 20*np.log10((np.sqrt(6)/2)*(2**12)*(2/3.3)))



