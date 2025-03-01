import numpy as np
import matplotlib.pyplot as plt

R = []
G = []
B = []

# Reading txt file and splitting data to own lists
with open("data/test.txt") as file:
    for line in file:
        line = line.split()
        
        R.append(float(line[0]))
        G.append(float(line[1]))
        B.append(float(line[2]))

fs = 30
N = 4096

R = np.array(R)
R -= np.mean(R)

dt = np.arange(0, len(R))*(1/fs)
df = np.linspace(-0.5, 0.5, N)*fs*60

pulse_spectrum = np.fft.fft(R, N)
pulse_spectrum = np.fft.fftshift(pulse_spectrum)

# plt.plot(df, abs(pulse_spectrum))
# plt.xlim(40, 240)
plt.plot(dt, R)
plt.show()

print(np.argmax(pulse_spectrum)-N/2)
