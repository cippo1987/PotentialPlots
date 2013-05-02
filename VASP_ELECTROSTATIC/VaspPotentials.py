import numpy
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.patches import Polygon
from scipy.interpolate import interp1d


Potential = numpy.zeros(shape=(224,2))
Macro = numpy.zeros(shape=(202,2))
# Open the file and split into Lines
f = open('POTPROF',"r")
lines = f.readlines()
f.close()
# Read in potetials
a=0
for line in lines:
 inp = line.split()
 Potential[a,0] = inp[0] 
 Potential[a,1] = inp[1]
 a=a+1

Potential_Interp=interp1d(Potential[:,0],Potential[:,1],kind='cubic')
# Read Macroscopic Potiential
f = open('MACROPOT',"r")
lines = f.readlines()
f.close()
a=0
for line in lines:
 inp = line.split()
 Macro[a,0] = inp[0] 
 Macro[a,1] = inp[1]
 a=a+1

Macro_Interp=interp1d(Macro[:,0],Macro[:,1],kind='cubic')
#plt.plot(Potential_Average[:,0],Potential_Average[:,1])
znew = np.linspace(min(Potential[:,0]),max(Potential[:,0]),500)
#plt.plot(znew,Potential_Interp(znew))
plt.plot(znew,Potential_Interp(znew),lw=3,color='black')
znew = np.linspace(min(Macro[:,0]),max(Macro[:,0]),500)
plt.plot(znew,Macro_Interp(znew),lw=1,color='r')
plt.show()
#plt.grid(True)
plt.show()

# Write the output

#print(Lattice)
#print(Coordinates)
#print(Potentials)
#f = open('Potentials.dat','w')
#for x in range(0,Potential_Array_Size):
# print '%4.2f %10.6f %i' % (Potential_Average[x,0], Potential_Average[x,1],Potential_Average[x,2])
# line = (Potential_Average[x,0], Potential_Average[x,1]) l = str(line)
# f.write(l)
#print(Potential_Average)
