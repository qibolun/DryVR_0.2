from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def ISS_dynamic(y,t,u1,u2,u3):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, y1, y2, y3 = y

    x1_dot = 0.77508*x2 - 1.5818e-8*u2 - 4.4341e-6*u3 - 3.9874e-8*x1 - 0.000067832*u1 - 0.000042976*x3 + 1.1479e-7*x4 - 7.09e-9*x5 - 1.653e-7*x6 + 0.000082292*x7 + 1.2158e-7*x8 - 0.000019112*x9 + 1.4896e-6*x10
    x2_dot = 0.010393*x3 - 7.046e-6*u2 - 0.0021408*u3 - 0.77508*x1 - 0.0077527*x2 - 0.029896*u1 - 0.000091911*x4 + 3.0412e-6*x5 + 0.000067451*x6 - 0.030171*x7 - 0.000093795*x8 + 0.0080792*x9 - 0.00062151*x10
    x3_dot = 0.025889*u1 + 5.692e-6*u2 + 0.0017739*u3 + 0.000042976*x1 + 0.010393*x2 - 0.019925*x3 + 1.992*x4 - 9.64e-6*x5 - 0.00020176*x6 + 0.074349*x7 + 0.00047222*x8 - 0.02434*x9 + 0.0018562*x10
    x4_dot = 0.00012603*u1 + 6.3733e-9*u2 - 8.2928e-6*u3 + 1.1344e-7*x1 + 0.000091528*x2 - 1.992*x3 - 4.721e-7*x4 + 6.8864e-8*x5 + 1.3712e-6*x6 - 0.00069225*x7 + 4.1564e-7*x8 + 0.00016249*x9 - 0.000011465*x10
    x5_dot = 1.6594e-6*u1 + 0.000049597*u2 - 5.5481e-6*u3 + 2.267e-9*x1 + 3.4178e-7*x2 + 1.4523e-6*x3 - 3.9616e-8*x4 - 2.0742e-7*x5 + 8.4808*x6 + 0.00019256*x7 - 8.1914e-6*x8 - 0.00027239*x9 + 4.7e-6*x10
    x6_dot = 0.000050285*u1 + 0.031956*u2 - 8.8146e-6*u3 + 8.4062e-8*x1 + 0.00002251*x2 - 0.000015118*x3 - 8.7922e-7*x4 - 8.4808*x5 - 0.084954*x6 + 0.0020235*x7 + 0.00035617*x8 - 0.00040077*x9 + 0.000061347*x10
    x7_dot = 0.074387*x3 - 0.00033453*u2 - 0.004295*u3 - 0.000082305*x1 - 0.030181*x2 - 0.06356*u1 + 0.00069032*x4 - 0.00015437*x5 + 0.00051015*x6 - 0.38083*x7 - 37.979*x8 + 0.7873*x9 - 0.060466*x10
    x8_dot = 0.00046227*u1 + 4.5013e-6*u2 - 0.000403*u3 + 4.9915e-7*x1 + 0.00023226*x2 - 0.00081483*x3 - 3.7771e-6*x4 + 6.7246e-6*x5 - 0.00034414*x6 + 37.981*x7 - 0.000035297*x8 + 0.00053662*x9 - 0.00070952*x10
    x9_dot = 0.0067388*u1 - 0.00010737*u2 - 0.029739*u3 + 7.2178e-6*x1 + 0.0017*x2 - 0.00019482*x3 - 0.00011165*x4 + 0.00019205*x5 + 0.00079526*x6 - 0.6624*x7 - 0.003324*x8 - 0.095564*x9 - 9.226*x10
    x10_dot = 0.000018473*u2 - 0.00049267*u1 + 0.0011629*u3 - 6.128e-7*x1 - 0.00015906*x2 + 0.000098378*x3 + 7.5464e-6*x4 - 2.7468e-6*x5 - 0.00014204*x6 + 0.050261*x7 + 0.00077848*x8 + 9.2327*x9 - 0.00016399*x10
    y1 = 0.000067947*x1 - 0.029964*x2 + 0.025941*x3 - 0.00012623*x4 + 6.5319e-6*x5 + 0.00013057*x6 - 0.06363*x7 - 0.00012503*x8 + 0.01654*x9 - 0.0012343*x10
    y2 = 5.5487e-9*x1 - 3.8275e-6*x2 + 3.2968e-6*x3 - 4.5505e-8*x4 - 0.000043816*x5 + 0.031956*x6 - 0.00020452*x7 - 8.8804e-6*x8 - 0.0001039*x9 + 0.000015029*x10
    y3 = 2.0132e-6*x1 - 0.00075046*x2 + 0.00065699*x3 + 4.4664e-6*x4 - 0.000023041*x5 + 0.000011699*x6 - 0.0031187*x7 - 0.00060035*x8 - 0.025617*x9 + 0.00026762*x10

    dydt = [x1_dot, x2_dot, x3_dot, x4_dot, x5_dot, x6_dot, x7_dot, x8_dot, x9_dot, x10_dot, y1, y2, y3]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.001;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    u1 = initialCondition[13]
    u2 = initialCondition[14]
    u3 = initialCondition[15]

    sol = odeint(ISS_dynamic, initialCondition[0:13], t, args=(u1,u2,u3), hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,10]))
        tmp.append(float(sol[j,11]))
        tmp.append(float(sol[j,12]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("Default", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9, 0.9], 20.0)
    #for s in sol:
	#	print(s)

    time = [row[0] for row in sol]

    a = [row[1] for row in sol]

    b = [row[2] for row in sol]

    plt.plot(time, a, "-r")
    plt.plot(time, b, "-g")
    plt.show()
    plt.plot(a, b, "-r")
    plt.show()
    