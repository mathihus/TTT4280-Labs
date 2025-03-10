import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

R = []
G = []
B = []

# Reading txt file and splitting data to own lists
with open("data/ref6.txt") as file:
    for line in file:
        line = line.split()
        
        R.append(float(line[0]))
        G.append(float(line[1]))
        B.append(float(line[2]))

def remove_offset(channel):
    channel = np.array(channel)
    channel -= np.mean(channel)

    return channel


def SNR(Sdb, f, B):
    noise_power = max(max(Sdb[:f-B]), max(Sdb[f+B:]))
    return -noise_power

def find_pulse(signal, N, plot=False):
    dt = np.arange(0, len(signal))*(1/fs)
    df = np.fft.fftfreq(N, d=1/fs)[:N//2]*60

    pulse_spectrum = np.fft.fft(signal, N)
    pulse_spectrum = abs(pulse_spectrum[:N//2])

    if plot:
        #plt.plot(df, 20*np.log10(pulse_spectrum/max(pulse_spectrum)))
        #plt.xlim(40, 240)
        plt.plot(t, signal)
        plt.show()

    freq_index = np.argmax(pulse_spectrum)
    detected_freq = df[freq_index]

    Sdb = 20*np.log10(pulse_spectrum/max(pulse_spectrum))

    signal_SNR = SNR(Sdb, freq_index, N//256)
    #print("SNR: ", signal_SNR)

    return detected_freq

def bandpass_filter(signal, fs, lowcut, highcut, order=4, window=1):
    nyq = fs / 2  # Nyquist frequency
    low = lowcut / nyq
    high = highcut / nyq

    # apllying window function, window=1 by default
    signal = signal*window
    
    # Butterworth bandpass filter
    b, a = butter(order, [low, high], btype='band')
    
    # Apply filter using filtfilt (zero-phase)
    filtered_signal = filtfilt(b, a, signal)
    
    return filtered_signal


R = remove_offset(R)
G = remove_offset(G)
B = remove_offset(B)

data_length = len(G)

fs = 30

# Artificial signal with 60 bpm
L = data_length
dt = 1/fs
f = 1

t = np.linspace(0, L-1, L)*dt
x = np.sin(2*np.pi*f*t)

# creating hanning window
n = np.linspace(0, data_length-1, data_length)
w = (np.sin(np.pi*n/ data_length))**2

def måling(signal):
    # Apply bandpass filter (0.67 Hz - 4 Hz) -> (40 bpm - 240 bpm) and hanning window on signal
    filtered_signal_hanning = bandpass_filter(signal, fs, 2/3, 4, window=w)
    filtered_signal = bandpass_filter(signal, fs, 2/3, 4)

    # Setting FFT length N
    N = 4*2048 

    print("Raw:", find_pulse(signal, N), "\n")
    print("Uten Hanning:", find_pulse(filtered_signal, N), "\n")
    print("Med Hanning:", find_pulse(filtered_signal_hanning, N), "\n")

print("Rød kanal:")
måling(R)

print("Grønn kanal:")
måling(G)

print("Blå kanal:")
måling(B)