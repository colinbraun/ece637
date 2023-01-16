#!/bin/python3
# Template file for ece 637 labs
import numpy as np
import matplotlib.pyplot as plt


def func(u, v):
    """
    Compute the value of the CTFT 
    """
    return np.sin(u*8*np.pi)*np.sin(v*8*np.pi)*2*2/81/81/np.pi/np.pi/u/v

figure = plt.figure()
axis = figure.add_subplot(111, projection='3d')

u = np.linspace(-1, 1, 1000)
v = np.linspace(-1, 1, 1000)
data = np.random.random((1000, 1000))
U, V = np.meshgrid(u, v)
z = np.array(func(U.ravel(), V.ravel()))
Z = z.reshape(U.shape)

axis.plot_surface(U, V, Z)
plt.show()

