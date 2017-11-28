from z3 import *
y = Real('y')
t = Real('t')
s = Solver()
s.add(And(y==0, t>=1/5))
s.add(t >= 3)
s.add(t <= 3.05)
s.add(y >= -0.1)
s.add(y <= 0.1)
print s
print s.check()
# [And(y <= 0, t >= 1/5, y >= -1/100),
#  t >= 143/100,
#  t <= 36/25,
#  y >= 731657374587/10000000000000,
#  y <= -674642625413/10000000000000,
#  velocity >= -7007/500,
#  velocity <= -1764/125]
