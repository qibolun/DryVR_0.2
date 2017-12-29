from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math

def uniform_inverter_loop(y,t,mode):
    v, stim = y
    v = float(v)
    stim = float(stim)

    