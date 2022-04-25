from modules.data_reader.Tecplot import Tecplot
import numpy as np
import matplotlib.pyplot as plt

# creating an empty figure for plotting
fig = plt.figure()

# defining a sub-plot with 1x2 axis and defining
# it as first plot with projection as 3D
ax = fig.add_subplot(1, 1, 1, projection='3d')

# creating a range of values for
# x1,y1  from -1 to 1 with
# a space of 0.1 between the elements so that
# we can create a single curve in the plot
x1 = np.arange(-1, 1, 0.1)
y1 = np.arange(-1, 1, 0.1)

# Creating a mesh grid with x ,y and x1,
# y1 which creates an n-dimensional
# array
x1, y1 = np.meshgrid(x1, y1)

# Creating a cosine function with the
# range of values from the meshgrid
z1 = np.cos(x1 * np.pi / 2)
extent = [x1.min(),x1.max(), y1.min(),y1.max(),z1.min(),z1.max()]
import copy
toplot = copy.deepcopy(z1)
toplot= z1/2



# Creating a wireframe plot with the points
#x1,y1,z1 along with the plot line as red
ax.plot_surface(x1, y1, z1/2, color="red")

ct = ax.contour3D(x1, y1, toplot, levels=[0.3,0.4])
plt.show()