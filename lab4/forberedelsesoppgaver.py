import numpy as np
c = 299792458

def dopplerskift(v_rad):
    f_d = (2*(24.13*10**9)*v_rad)/c
    return f_d

def måleoppløsning(T):
    dirac_v = 1/T
    return dirac_v

def antennevinning(deg_azi, deg_elev):
    G = 10*np.log10((30000/(deg_azi*deg_elev)))
    return G

def sigma(a, f_0):
    bølgelengde  = c/(f_0)
    sigma = (4*np.pi*((a)**4))/(4*(bølgelengde**2))
    return sigma

def R(phi, f_0):
    bølgelengde  = c/(f_0)
    R = phi*bølgelengde/(2*2*np.pi)
    return R 

print("foreberedelse 2.1.1: ",dopplerskift(25))
print("foreberedelse 2.1.2: ",måleoppløsning(1))
print("foreberedelse 2.1.3: ",antennevinning(12, 80))
print("foreberedelse 2.1.4: ",sigma(0.155, (24*(10**9))))



