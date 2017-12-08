from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/lac-operon/ 

def lac_operon_dynamic(y,t):
    I, G = y
    I = float(I)
    G = float(G)

    I_dot = -2 * k_3 * I**2 * (k_8 * R_i * G**2 + t)/(k_3 * I**2 + )
