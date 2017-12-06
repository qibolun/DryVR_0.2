
# coding: utf-8

# In[126]:

file = open("output/Traj.txt","r")


# In[127]:

x = file.readlines()


# In[ ]:




# In[128]:

xcoord = []
ycoord = []
car_1x = []
car_1y = []
for a in x:
    splitted =  a.split()
    if len(splitted)<5:
        continue
    else:
        xcoord.append(splitted[6])
        ycoord.append(splitted[7])
        car_1x.append(splitted[1])
        car_1y.append(splitted[2])


# In[129]:

import matplotlib.pyplot as plt


# In[130]:

plt.plot(xcoord,ycoord,"-k",label = "car2")
plt.plot(car_1x,car_1y,"y",label = "car1")
plt.legend(("car2","car1"))


# In[131]:

plt.show()


# In[ ]:



