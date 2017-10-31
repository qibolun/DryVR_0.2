from z3 import *
from math import *
# car1_x = Real('car1_x')
# car1_y = Real('car1_y')
# car2_x = Real('car2_x')
# car2_y = Real('car2_y')
# c1 = car1_x-car2_x<1
# c2 = car2_x-car1_x<1
# c3 = car1_y-car2_y<-10
# c4 = car1_y-car2_y>-40

car1_x = 1
car1_y = 2
car2_x = 3
car2_y = 4

equ = "dis=sqrt((car2_x-car1_x)**2 + (car2_y-25-car1_x)**2)"
exec(equ)
# dis = sqrt((car2_x-car1_x)**2 + (car2_y-25-car1_x)**2)
print dis