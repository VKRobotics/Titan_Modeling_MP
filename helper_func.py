import math
import constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def p_density(h):
    return constants.RHO_0*np.exp(-h / constants.H_SCALE)
def g_accel(h):
    return constants.G * constants.MASS_T / (constants.RAD_T + h)**2
def cda(h,V):
    if h > constants.H_DEPLOY_MAIN:
        c=speed_sound_interpol(h)
        mach=V/c
        if mach<=0.5:
            return 0.93*constants.A_CAP
        elif mach<=1.5:
            cd=0.93+0.55*((3*(mach-0.5)**2)-2*(mach-0.5)**3)
            return cd*constants.A_CAP
        else:
            return 1.48*constants.A_CAP
    elif h > constants.H_DEPLOY_DROGUE:
        return constants.CDA_PHASE1   # main parachute open
    else:
        return constants.CDA_PHASE2   # drogue / stabiliser
    

def dV_dt(V, gamma, h):
    drag   = (p_density(h) * cda(h,V) * V**2) / (2 * constants.MASS_P)
    grav   = g_accel(h) * np.sin(gamma)
    return -drag + grav
def dgamma_dt(V, gamma, h):
    r = constants.RAD_T + h
    centripetal = V**2 / r
    gravity     = g_accel(h)
    return ((-centripetal + gravity) * (np.cos(gamma))) / V
 
 
def dh_dt(V, gamma):
    return -V * np.sin(gamma)


atmo_data=pd.read_csv("compiled_data.csv")
altitude=(atmo_data['ref_alt (kilometers)'].values*1000.0)[::-1]
speed_sound=atmo_data['speed_of_sound (m/s)'].values[::-1]

def speed_sound_interpol(h):
    return np.interp(h,altitude,speed_sound)