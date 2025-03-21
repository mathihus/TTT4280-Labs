from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('data/speed2.bin') # converting binary file to array with raspi_import.py

data -= (2**12-1)/2 #+16.5 # subtracting offset
data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt

second_interval = 5 # only 1-9 are valid inputs

sample_start = data.shape[0]//(11-second_interval)
sample_stop = data.shape[0]//(10-second_interval)

Q, I = data[sample_start:sample_stop, 3], data[sample_start:sample_stop, 4]

data_length = len(Q) # getting the length of samples

n = np.arange(data_length) # making a list with same length as data to be the x-axis of plotting later
time = n*(sample_period) # scaling x-axis to time in seconds

w = np.sin(np.pi*n/ data_length)**2 # hanning window function

c = 299792458
f_0 = 24.13*10**9

def fft(signal, N):
    spectrum = abs(np.fft.fft(signal, N)) # reshaping data to be an 1d array and taking fft
    spectrum = abs(np.fft.fftshift(spectrum)) # shifting spectrum and taking absolute value 
    
    normalised_spectrum = 20*np.log10(spectrum/max(spectrum))
    return normalised_spectrum

def v_rad(f_d):
    v = (c*f_d)/(2*f_0)
    return v

def plotter(time, frequency, signal, spectrum):

    plt.plot(time, np.real(signal))
    plt.plot(time, np.imag(signal))
    plt.show()

    plt.plot(frequency, spectrum)
    plt.xlim(-1000, 1000)
    plt.ylim(-50, 5)
    plt.show()

N = 2**18 # setting FFT length to closest 2 power of data_length
# N = data_length

fs = int(1/sample_period) # samplings frequency
df = np.linspace(-0.5, 0.5, N)*fs # making scaled frequency axis

dopler = I+(1j*Q)
# dopler = dopler*w
dopler_spectrum = fft(dopler, N)

plotter(time, df, dopler, dopler_spectrum)

f_d = df[np.argmax(dopler_spectrum)]
print(f_d, "Hz")
speed = v_rad(f_d)
print(speed, "m/s")
# print(speed*3.6, "km/h")