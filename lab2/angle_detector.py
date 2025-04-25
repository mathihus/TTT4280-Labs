from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as scp

def lag(signal1, signal2, mic, interp=1):
    corr = np.correlate(signal1, signal2, "full")

    lag_n = len(signal1)  

    if interp==1:
        # finding lag estimate from the correlation
        lag_estimate = (np.argmax(corr))-len(corr)//2

        plt.plot(-(np.arange(len(corr))-lag_n+1), corr, ".", label=mic)
        plt.title("Krysskorrelasjon uten interpolasjon")
    else:
        # making new scaled x axis with interp times more points
        x = np.arange(len(corr))
        x_new = np.linspace(0, len(corr)-1, len(corr)*interp)
        # x_new = np.arange(len(corr)*interp)

        # making interpolated crosscorrelation sequence
        interp_corr = scp.interp1d(x, corr, kind='cubic')
        interpcorr = interp_corr(x_new)

        # finding lag estimate from the interpolated correlation
        lag_estimate = (np.argmax(interpcorr))-len(interpcorr)//2 +1

        plt.plot(-(x_new+1-lag_n)*interp, interpcorr, ".", label=mic)
        plt.title(f"Krysskorrelasjon med {interp}x interpolasjon")
    
    plt.xlim((-8*interp, 8*interp))
    plt.ylim(0, 200)
    return -lag_estimate

def angle(signal1, signal2, signal3, plot=False, interpolation_factor=1):
    # Finding all the lags
    n21 = lag(signal2, signal1, r"$r_{31}$", interp=interpolation_factor)
    n31 = lag(signal3, signal1, r"$r_{21}$", interp=interpolation_factor)
    n32 = lag(signal3, signal2, r"$r_{32}$", interp=interpolation_factor)

    print(f"n21 = {n21}, n31 = {n31}, n32 = {n32}")

    # plotting the cross correlations if plot=True
    if plot:
        plt.legend()
        plt.xlabel("Punktprøve")
        plt.ylabel("Korrelasjon")
        plt.show()

    # calculating angle
    angle_estimate = -np.arctan(np.sqrt(3)*((n31+n21)/(n31-n21+2*n32)))


    # adding pi if denominator is negative
    if (n31-n21+2*n32) < 0:
        angle_estimate += np.pi

    # allowing angles slightly higher than pi for statistical reasons
    if angle_estimate > 1.1*np.pi:
        angle_estimate -= 2*np.pi

    return angle_estimate

def angle_detect(deg, i, plot=False, interpolation_factor=1):
    sample_period, data = raspi_import(f'data/{deg}/{deg}_deg_{i}.bin') # converting binary file to array with raspi_import.py

    data -= (2**12-1)/2 # subtracting offset
    data = data*(3.3/((2**12)-1)) # scaling y-axis to Volt for plotting of time signal

    skip_samples = 3000 # skipping the first x samples to get rid off noise at the start of sampling
    end_samples = len(data[:, 0])-10000

    signal1, signal2, signal3 = data[skip_samples:end_samples, 2], data[skip_samples:end_samples, 0], data[skip_samples:end_samples, 1]

    if plot:
        fig, ax = plt.subplots(3, 1) # setting up figure to put subplots of time series
        fig.tight_layout(pad=0.5)

        time = np.arange(len(signal1))*sample_period

        for i in range(3): # Plotting data channel i
            ax[i].plot(time, data[skip_samples:end_samples, i])
            ax[i].set_title(f"Mikrofon {i+1}:")
            ax[i].set_ylim(-2, 2)
            # ax[i].set_xlim(0.70, 0.75)
            ax[i].set_ylabel("Amplitude [V]")
            ax[i].set_xlabel("Tid [s]")

        plt.show()

    angle_estimate = angle(signal1, signal2, signal3, plot, interpolation_factor) 
    
    return (angle_estimate*180/np.pi) # taking absolute angle and converitng to degrees from rad


def create_angle_matrix(interpolation_factor=1):

    angles = np.zeros((8, 5))

    for i in range(8):
        for n in range(5):
            a = angle_detect(45*i, n+1, interpolation_factor=interpolation_factor)
            angles[i, n] = a

    np.savetxt(f"angle_estimates_matrix_{interpolation_factor}.csv", angles, delimiter=";")
    return angles



def lag_to_angle(lag1, lag2, lag3):
    
    angle_estimate = -np.arctan(np.sqrt(3)*((lag2+lag1)/(lag2-lag1+2*lag3)))

    if (lag2-lag1+2*lag3) < 0:
        angle_estimate += np.pi
    if angle_estimate > 1.2*np.pi:
        angle_estimate -= 2*np.pi

    return angle_estimate*180/np.pi

def all_possible_lags(max_lags):
    angles = []
    
    for i in range(-max_lags, max_lags+1):
        for n in range(-max_lags, max_lags+1):
            for k in range(-max_lags, max_lags+1):
                try:
                    a = lag_to_angle(i, n, k)
                    angles.append(a)
                    # print(i, n, k, ":", a)
                except:
                    pass
    
    return set(angles)


def create_angle_matrix_2(interpolation_factor=1):
    d = 2

    angles = np.zeros((8, d*5))

    for i in range(8):
        for n in range(0, d*5, d):
            a = angle_detect(45*i, n//d+1, interpolation_factor=interpolation_factor)
            for k in range(d):
                angles[i, n+k] = a

    np.savetxt("more_angle_estimates.csv", angles, delimiter=";")
    return angles


# angles = all_possible_lags(4)
# print(angles)

# create_angle_matrix(1)
# create_angle_matrix(4)
# create_angle_matrix(8)

print(angle_detect(45, 4, True, 1))
# print(angle_detect(90, 3, True, 2))
# print(angle_detect(90, 3, True, 4))
print(angle_detect(90, 5, True, 8))

# for i in range(8):
#     print(f"Actual angle: {45*i} - Meassured angle: {angle_detect(45*i, 2)} \n")

