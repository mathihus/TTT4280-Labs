import numpy as np


muabo = np.genfromtxt("./muabo.txt", delimiter=",")
muabd = np.genfromtxt("./muabd.txt", delimiter=",")

red_wavelength = 600 # Replace with wavelength in nanometres
green_wavelength = 515 # Replace with wavelength in nanometres
blue_wavelength = 460 # Replace with wavelength in nanometres

wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

def mua_blood_oxy(x): return np.interp(x, muabo[:, 0], muabo[:, 1])
def mua_blood_deoxy(x): return np.interp(x, muabd[:, 0], muabd[:, 1])

bvf = 0.01 # Blood volume fraction, average blood amount in tissue
oxy = 0.8 # Blood oxygenation

# Absorption coefficient ($\mu_a$ in lab text)
# Units: 1/m
mua_other = 25 # Background absorption due to collagen, et cetera
mua_blood = (mua_blood_oxy(wavelength)*oxy # Absorption due to
            + mua_blood_deoxy(wavelength)*(1-oxy)) # pure blood
mua = mua_blood*bvf + mua_other
mua2 = mua_blood*bvf*100 + mua_other

# reduced scattering coefficient ($\mu_s^\prime$ in lab text)
# the numerical constants are thanks to N. Bashkatov, E. A. Genina and
# V. V. Tuchin. Optical properties of skin, subcutaneous and muscle
# tissues: A review. In: J. Innov. Opt. Health Sci., 4(1):9-38, 2011.
# Units: 1/m
musr = 100 * (17.6*(wavelength/500)**-4 + 18.78*(wavelength/500)**-0.22)

# mua and musr are now available as shape (3,) arrays
# Red, green and blue correspond to indexes 0, 1 and 2, respectively

# TODO calculate penetration depth
def pen_depth():
    pen = np.sqrt(1/(3*(musr+mua)*mua))
    return pen

print("\na) \nPenetrasjonsdybde i mm for R, G og B:", pen_depth()*1000)


def T(z, m):
    C = np.sqrt(3*m*(musr+m))
    return np.exp(-C*z)

d = 0.012 # fingerdybden i meter
print("\nb) \nTransmittans med tykkelse", d, "i prosent for R, G og B:", T(d, mua)*100)

print("Forventer at det meste av lyset for hver bølgelengde penetrerer ned til penetrasjonsdybden eller kortere før den reflekteres. Det som går lenger dempes fort. Se oppgave a :)")

def R(z):
    C = np.sqrt(3*mua*(musr+mua))
    return (1/(pen_depth()*mua))*np.exp(-2*C*z)

# print(R(pen_depth()))

def K(høy, lav):
    return abs(høy-lav)/lav

bd = 300*1e-6
T_høy = T(bd, mua2)
T_lav = T(bd, mua)

print("\nd) \nTransmittans blodåre i prosent for R, G og B:", T_høy*100)
print("Transmittans vev i prosent for R, G og B:", T_lav*100)
print("Kontrast K =", K(T_høy, T_lav))

print("\ne) \nGrønn kanal vil være best ettersom den har har tilnærmet samme kontrast som blå K = 0.99 og er det mest sensitive kanalen på rasberry pi kameraet. En høy K vil gi en høy pulsamplitude.")

print("\n2.2 \nSNR i bildekvalitetssammenheng. Snittsignalnivå over bildet delt på standardavviket til støyen i bildet, mu_signal1/sigma_imagenoise. Uttrykker generell bildekvalitet. Interessesignalet er pikselverdien. \n\nSNR i pulssammenheng. Maksamplitude i pulssignalet delt på standardavviket til støyen i pulssignalet, mu_signal2/sigma_pulsenoise. Uttrykker kvaliteten på pulsutslaget, hvor begravd pulssignalet er i støy, hvor lett det er å estimere puls. Interessesignalet er pikselvariasjonen knyttet til puls.")
print("\nVi antar at støyen har høyere frekvens enn en realistisk pulsmåling, og lavere amplitude. Ved å ta FFT kan man da kutte ut frekvensene som ikke er realistiske, og se på maksimalverdien innenfor dette området.")