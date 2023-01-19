#!/bin/python3
# Template file for ece 637 labs
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from PIL import Image


def func(u, v):
    """
    Compute the value of the CTFT 
    """
    return np.sin(u*8*pi)*np.sin(v*8*pi)*2*2/81/81/pi/pi/u/v

def func2(u, v):
    """
    Section 3 function to be plotted
    """
    return 1/81 * (2*np.cos(u) + 2*np.cos(2*u) + 2*np.cos(3*u) + 2*np.cos(4*u) + 1) * (2*np.cos(v) + 2*np.cos(2*v) + 2*np.cos(3*v) + 2*np.cos(4*v) + 1)

def func3(u, v, lam=1.5):
    """
    Section 4 function to be plotted
    """
    h = 1/25 * (2*np.cos(u) + 2*np.cos(2*u) + 1) * (2*np.cos(v) + 2*np.cos(2*v) + 1)
    return 1 + lam * (1 - h)

def func4(u, v):
    """
    Section 5 function to be plotted
    """
    return np.absolute(0.01 * (np.exp(1j*u)*np.exp(1j*v)) / (np.exp(1j*u)*np.exp(1j*v) - 0.9*np.exp(1j*u) - 0.9*np.exp(1j*v) + 0.81))


figure = plt.figure()
axis = figure.add_subplot(111, projection='3d')

u = np.linspace(-pi, pi, 1000)
v = np.linspace(-pi, pi, 1000)
# data = np.random.random((1000, 1000))
U, V = np.meshgrid(u, v)
# ----------------SECTION 3 PLOTTING-----------------
z = np.array(func2(U.ravel(), V.ravel()))
Z = z.reshape(U.shape)

axis.plot_surface(U, V, Z)
plt.savefig("section3-python.png")
# plt.show()

#---------------------SECTION 4 PLOTTING--------------
z = np.array(func3(U.ravel(), V.ravel()))
Z = z.reshape(U.shape)

figure = plt.figure()
axis = figure.add_subplot(111, projection='3d')
axis.plot_surface(U, V, Z)
plt.savefig("section4-python.png")
# plt.show()

#--------------------SECTION 5 PLOTTING--------------
z = np.array(func4(U.ravel(), V.ravel()))
Z = z.reshape(U.shape)

figure = plt.figure()
axis = figure.add_subplot(111, projection='3d')
axis.plot_surface(U, V, Z)
plt.savefig("section5-python.png")
# plt.show()

#--------------------SECTION 5 POINT SPREAD----------
y = np.zeros([256, 256])
y[0, 0] = 0.01
# print(image)
for row in range(256):
    for col in range(256):
        if row == 0 and col == 0:
            continue
        # Careful about indexing negative values. Here it is fine, since the last few entries are 0 to start anyway.
        y[row, col] = 0.9 * (y[row-1, col] + y[row, col-1]) - 0.81 * y[row-1, col-1]

print(y*255*100)
imsave = Image.fromarray((255*100*y).astype(np.uint8))
imsave.save('h_out.tif')
