import numpy
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.patches import Polygon
from scipy.interpolate import interp1d

copy = 0
a = 0
Bin_Width=2
Potential_Array_Size=0
Metal='Mg1'

# Open the file and split into Lines
f = open('GOUT',"r")
lines = f.readlines()
f.close()

num_ox = 0

for line in lines:
 inp = line.split()
 if inp == []:
  continue
 if len(inp) == 6 and inp[2] == "irreducible":
  num_atoms = inp[5]
 if len(inp) == 5 and inp[0] == "Dimensionality":
  dimensions = int(inp[2])
num_atoms=int(num_atoms)
#print("Number of dimensions:", dimensions)
Potentials = numpy.zeros(shape=(num_atoms))
Lattice = numpy.zeros(shape=(3,3))
Coordinates=numpy.zeros(shape=(num_atoms,3))
#Get the data we require
for line in lines:
 inp = line.split()
 if inp == []:
  continue
# Get the Madelung potetnials out
 if inp[0] == 'Electrostatic':
  copy = 1
 if inp[0] == 'Electric':
  copy = 0
 if copy == 1 and len(inp) == 7 and inp[1] == 'O1':
  num_ox = num_ox+1
  Potentials[a] = inp[3]
  a = a + 1
# Get the lattice vectors
a = 0
copy = 0
for line in lines:
 inp = line.split()
 if dimensions == 3:
  if inp == []:
   continue
  if inp[0] == "Cartesian" and inp[1] == "lattice":
   copy=1
  if inp[0] == "Cell" and copy == 1:
   copy=0
  if copy == 1 and len(inp) == 3:
   Lattice[a] = inp
   a=a+1
  elif dimensions == 2:
   if len(inp) == 5 and inp[1] == "Cartesian":
    copy = 1
   if copy == 1 and inp[1] == "cell":
    copy = 0
   if copy == 1 and len(inp) == 3:
    Lattice[a] = inp
    a = a + 1
#Get the coordinates
a = 0
copy = 0
for line in lines:
 inp = line.split()
 if inp == []:
  continue
 if inp[0] == "Fractional" or inp[0] == "Mixed":
  copy=1
 if inp[0] == "Species" and copy == 1:
  copy=0
 if copy == 1 and len(inp) == 8 and inp[1] == "O1":
  Coordinates[a]=inp[3:6]
  a = a + 1
# Make coordinates cartesian
for x in range(0,num_atoms):
 Coordinates[x,0]=Coordinates[x,0]*Lattice[0,0]
 Coordinates[x,1]=Coordinates[x,1]*Lattice[1,1]
 if dimensions == 3:
  Coordinates[x,2]=Coordinates[x,2]*Lattice[2,2]
# Put the Potentials into bins of real space in z


if dimensions == 3:
# 3D Case
 Potential_Array_Size=int(math.ceil(Lattice[2,2]/Bin_Width))+4
elif dimensions == 2:
# 2D Case
 Potential_Array_Size=int(math.ceil((max(Coordinates[:,2])+15-min(Coordinates[:,2]))//Bin_Width))
Potential_Average=numpy.zeros(shape=(Potential_Array_Size,3))

for x in range(0,Potential_Array_Size):
 Potential_Average[x,0]=(x-2)*Bin_Width
 for y in range(0,num_ox):
  if Coordinates[y,2] >= Potential_Average[x,0] and Coordinates[y,2] < Potential_Average[x,0]+Bin_Width:
   Potential_Average[x,1]=Potential_Average[x,1]+Potentials[y]
   Potential_Average[x,2]=Potential_Average[x,2]+1

for x in range(0,Potential_Array_Size):
 if Potential_Average[x,2] > 0:
  Potential_Average[x,1]=Potential_Average[x,1]/Potential_Average[x,2]

Potential_Interp=interp1d(Potential_Average[:,0],Potential_Average[:,1],kind='slinear')
plt.plot(Potential_Average[:,0],Potential_Average[:,1])
plt.show()
znew = np.linspace(min(Potential_Average[:,0]),max(Potential_Average[:,0]),500)
plt.plot(znew,Potential_Interp(znew))
plt.grid(True)
plt.show()

# Write the output

#print(Lattice)
#print(Coordinates)
#print(Potentials)
#f = open('Potentials.dat','w')
#for x in range(0,Potential_Array_Size):
# print '%4.2f %10.6f %i' % (Potential_Average[x,0], Potential_Average[x,1],Potential_Average[x,2])
print "Average",sum(Potential_Average[:,1])/len(Potential_Average[:,1])
# line = (Potential_Average[x,0], Potential_Average[x,1]) l = str(line)
# f.write(l)
#print(Potential_Average)
