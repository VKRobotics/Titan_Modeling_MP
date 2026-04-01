import math
import constants
import numpy as np
import matplotlib.pyplot as plt


def p_density(h):
    return constants.RHO_0*np.exp(-h / constants.H_SCALE)
def g_accel(h):
    return constants.G * constants.MASS_T / (constants.RAD_T + h)**2
def cda(h):
    if h > constants.H_DEPLOY_MAIN:
        return constants.CDA_PHASE0   # no parachute yet
    elif h > constants.H_DEPLOY_DROGUE:
        return constants.CDA_PHASE1   # main parachute open
    else:
        return constants.CDA_PHASE2   # drogue / stabiliser
    

def dV_dt(V, gamma, h):
    """
    How fast is speed changing?  (m/s per second)
 
    Two forces act along the direction of travel:
      1. Aerodynamic drag  → always opposes motion, always negative
      2. Gravity component → during descent (gamma < 0):
                              -g * sin(negative) = POSITIVE
                              so gravity actually SPEEDS UP the craft
                              (until drag becomes large enough to win)
    """
    drag   = (p_density(h) * cda(h) * V**2) / (2 * constants.MASS_P)
    grav   = g_accel(h) * np.sin(gamma)
    return -drag - grav
def dgamma_dt(V, gamma, h):
    r = constants.RAD_T + h
    centripetal = V**2 / r
    gravity     = g_accel(h)
    return ((centripetal - gravity) * np.cos(gamma)) / V
 
 
def dh_dt(V, gamma):
    return V * np.sin(gamma)
