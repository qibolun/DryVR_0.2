from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math

def uniform_NOR_ramp_dynamic(y,t,mode):
    Vm, Vout, stim = y
    Vm = float(Vm)
    Vout = float(Vout)
    stim = float(stim)

    if mode == "NOR_Rampup":
        Vm_dot = 0.18688194*(-(0.172331258975586*math.pow(5.2360277794589, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.73000000028971)*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6)) - 0.18688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        Vout_dot = -0.0004722975*(-(0.0686008289266829*math.pow(1.00001997216919, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 1.3701073619532e-6)*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6)) - 0.0004722975*(-(0.0686008289266829*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 0.039*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1))*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6)) + 0.00018688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        stim_dot = 1
    elif mode == "NOR_On":
        Vm_dot = 0.18688194*(-(0.172331258975586*math.pow(5.2360277794589, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.73000000028971)*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6)) - 0.18688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        Vout_dot = -0.0004722975*(-(0.0686008289266829*math.pow(1.00001997216919, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 1.3701073619532e-6)*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6)) - 0.0004722975*(-(0.0686008289266829*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 0.039*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1))*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6)) + 0.00018688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        stim_dot = 0
    elif mode == "NOR_Rampdown":
        Vm_dot = 0.18688194*(-(0.172331258975586*math.pow(5.2360277794589, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.73000000028971)*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6)) - 0.18688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        Vout_dot = -0.0004722975*(-(0.0686008289266829*math.pow(1.00001997216919, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 1.3701073619532e-6)*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6)) - 0.0004722975*(-(0.0686008289266829*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 0.039*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1))*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6)) + 0.00018688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        stim_dot = -1
    elif mode == "NOR_Off":
        Vm_dot = 0.18688194*(-(0.172331258975586*math.pow(5.2360277794589, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.73000000028971)*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-Vm + 1.2)/(0.344662517951173*math.pow(5.2360277794589, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(-Vm - 0.344662517951173*math.pow(5.2360277794589, 0.5) + 2.54466251795117) + 6.0e-6)) - 0.18688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        Vout_dot = -0.0004722975*(-(0.0686008289266829*math.pow(1.00001997216919, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 1.3701073619532e-6)*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(1.00001997216919, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(1.00001997216919, 0.5) + 1.13720165785337) + 6.0e-6)) - 0.0004722975*(-(0.0686008289266829*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 0.039*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1))*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*Vout/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vout - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6)) + 0.00018688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(Vm - Vout)/(0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(Vm - Vout - 0.344662517951173*math.pow(0.226308333333333*math.log(5.83706736205705e-6*math.exp(25.6410256410256*Vm - 25.6410256410256*stim) + 1) + 1, 0.5) + 1.34466251795117) + 6.0e-6))
        stim_dot = 0
    
    dydt = [Vm_dot, Vout_dot, stim_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.00002;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(uniform_NOR_ramp_dynamic, initialCondition, t, args=(Mode,),hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        tmp.append(float(sol[j,2]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("NOR_Rampup", [0.75,1.15,0.0], 6.4)
    #for s in sol:
	#	print(s)
    time = [row[0] for row in sol]

    v = [row[1] for row in sol]

    stim_local = [row[2] for row in sol]

    plt.plot(v,stim_local,"-r")
    plt.show()