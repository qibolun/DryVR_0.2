file = open('output/Traj.txt')

import matplotlib.pyplot as plt

labelPos = []
curT = 0.0
trace = []
unsafeT = []
for line in file:
	line = line.strip()
	if line[0].isalpha():
		labelPos.append((curT,line))
		continue

	line = map(float,line.split(' '))
	if trace == []:
		dim = len(line)
		trace = [[] for _ in range(dim)]

	curT = line[0]
	for idx,val in enumerate(line):
		trace[idx].append(val)
	if (abs(line[6]-line[2])<=2 or abs(line[2]-line[6])<=2) and (abs(line[5]-line[1])<=2 or abs(line[1]-line[5])<=2):
		unsafeT.append(line[0])

minT = min(unsafeT)
maxT = max(unsafeT)

print labelPos
f, ax = plt.subplots(2, 1, sharex=True)
l1, = ax[0].plot(trace[0],trace[2], color="blue", label='Car')
l2, = ax[0].plot(trace[0],trace[6], color="red", label='Bike')
ax[0].axvspan(minT, maxT, alpha=0.5, color='grey')
ax[0].legend(handles=[l1, l2])
ax[0].set_title("time vs sy")
ax[1].plot(trace[0],trace[1], color="blue", label='Car')
ax[1].plot(trace[0],trace[5], color="red", label='Bike')
ax[1].axvspan(minT, maxT, alpha=0.5, color='grey')
ax[1].legend(handles=[l1, l2])
ax[1].set_title("time vs sx")
for time,label in labelPos:
	ax[0].axvline(time, color='black', linestyle='--')
	ax[1].axvline(time, color='black', linestyle='--')




plt.show()

