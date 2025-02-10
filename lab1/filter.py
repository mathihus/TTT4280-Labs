import matplotlib.pyplot as plt
import numpy as np

L = 100e-3
C = 470.1e-6

ft = np.linspace(2, int(1e6), int(1e7))

Ht = abs(1/(1-(L*C*(2*np.pi*ft)**2)))

plt.plot(ft, 10*np.log(Ht), label=r"Teoretisk |$H(f)$|")
plt.plot(ft, np.zeros(len(ft))-3, "-", label="-3dB knekkfrekvens")
# plt.xscale("log")
# plt.show()

Hm = []
fm = []

with open("Pifilter.csv", "r") as file:
    for line in file:
        line = line.split(",")
        print(line)
        fm.append(float(line[0]))
        Hm.append(float(line[1]))        


plt.plot(fm, Hm, label=r"Målt |$H(f)$|")
plt.xscale("log")
plt.xlabel("Frekvens, [Hz]")
plt.ylabel("Amplitude, [dB]")
plt.xlim(3, 1e3)
plt.ylim(-100, 70)

plt.title("Amplituderespons av Pi-filter")
plt.legend()
plt.show()