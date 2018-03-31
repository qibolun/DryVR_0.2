
from InOutput import *
import matplotlib.pyplot as plt
from simulate import *
from TC_Graph import *

g = takeOverGraph()

# Sim_Result = read_from_file('output/TC_Traj.txt','simulation')
Initial = [0.0,0.0,0.0,1.0,0.0,-15.0,0.0,1.0]
Sim_Result = simulate(g,Initial,50)
time = [row[0] for row in Sim_Result]
sx = [row[1]-row[5] for row in Sim_Result]
sy = [row[2]-row[6] for row in Sim_Result]
vx = [row[3]-row[7] for row in Sim_Result]
vy = [row[4]-row[8] for row in Sim_Result]
# sx = [row[1] for row in Sim_Result]
# sy = [row[2] for row in Sim_Result]
# vx = [row[3] for row in Sim_Result]
# vy = [row[4] for row in Sim_Result]

v = [(row[3]**2 + row[4]**2)**0.5 for row in Sim_Result]

#print(Sim_Result)

plt.figure(1)
plt.subplot(211)
plt.plot(time,sx,'-r')
plt.plot(time,sy,'-g')

plt.subplot(212)
plt.plot(time,vx,'-r')
plt.plot(time,vy,'-g')
plt.plot(time,v,'-k')
plt.show()
plt.savefig('a.eps',format='eps',dpi=1200)

# Sim_Result = Car_simulate('Acc1', [0.0,0.0,0.0,1.0],5)
# vy = [row[4] for row in Sim_Result]
# print vy


'''
from Global_Disc import *
from InOutput import *

k,gamma = Global_Discrepancy('Acc2;Const',[0.0, 2.5000979815797368, 0.0, 0.0, 0.0, 1.7500000000014246, 0.0, 0.0], 0, 8)
#Current_reachtube = Bloat_to_tube('Startup', k, gamma, [0.01,0.1,0.01,0.05], 'output/Reachtube')

#lower,upper = Reachtube_trunk(Current_reachtube, [0.1,8])

print k
print gamma
'''

'''
from PW_Discrepancy import *

PW_Bloat_to_tube('Acc1;Const', [0.1000,0.1000,0.1000,0.2000,0.1000,1.0000,0.1000,0,2000], 1, 8, 'output/Reachtube','new')
'''

'''
from InOutput import *
import matplotlib.pyplot as plt

from TC_Graph import *
#g = mergeGraph()

g = takeOverGraph()

num_ver = g.vcount()

dim = 1

f, axarr = plt.subplots(num_ver, sharex=False)
# f, axarr = plt.subplots(1, sharex=False)
for vertex in range(num_ver):
	Current_reachtube = read_from_file('output/Reachtube'+g.vs[vertex]['name']+str(vertex)+'.txt', 'reachtube_single')
	time = [row[0] for row in Current_reachtube]
	value = [row[dim] for row in Current_reachtube]
	t = [time[i] for i in range(0,len(value),2)]
	lower_trace = [value[i] for i in range(0,len(value),2)]
	upper_trace = [value[i+1] for i in range(0,len(value),2)]

	axarr[vertex].plot(t, lower_trace,'o')
	axarr[vertex].plot(t, upper_trace,'o')
plt.show()
'''