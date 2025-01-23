import matplotlib.pyplot as plt
import numpy as np

L = 100e-3
C = 470.1e-6

ft = np.linspace(2, int(1e6), int(1e7))

Ht = abs(1/(1-(L*C*(2*np.pi*ft)**2)))

plt.plot(ft, 10*np.log(Ht))
plt.plot(ft, np.zeros(len(ft))-3, "-")
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


plt.plot(fm, Hm)
plt.xscale("log")
plt.xlabel("Frekvens, [Hz]")
plt.ylabel("Amplitude, [Hz]")
plt.show()