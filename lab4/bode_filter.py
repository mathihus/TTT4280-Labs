import csv
import matplotlib.pyplot as plt

def plot_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        frequency = []
        #channel1 = []
        channel2 = []
        
        for row in reader:
            frequency.append(float(row['Frequency (Hz)']))
            #channel1.append(float(row['Channel 1 Magnitude (dB)']))
            channel2.append(float(row['Channel 2 Magnitude (dB)']))
    
    #plt.plot(frequency, channel1, label="Channel 1")
    plt.plot(frequency, channel2, label="Channel 2")

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")

    plt.grid(True)

    plt.axvline(x=3.5, linestyle=':', color='r', label='f_c1')
    plt.axvline(x=2800, linestyle=':', color='r',label='f_c2')
    plt.axhline(y=(20-3), linestyle=':', color='g', label='-3dB')

    plt.legend()

    plt.ylim(0,25)
    plt.xlim(2,20000)

    plt.xscale('log')

    plt.show()


plot_from_csv('lab4/data/1vamplitude.csv')
plot_from_csv('lab4/data/1vamplitudemedelektronlytt.csv')
