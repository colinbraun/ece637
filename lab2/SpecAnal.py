#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:54:16 2021

@author: Wenrui Li
"""

import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.

def BetterSpecAnal(x):
    y_center = int(len(x)/2)
    x_center = int(len(x[0])/2)

    # Size of blocks
    block_size = 64
    # Number of blocks
    num_blocks = 25

    # Create the Hamming window
    hw = np.outer(np.hamming(block_size), np.hamming(block_size))
    total_pwr_spec_density = np.zeros([block_size, block_size])
    # windows = []
    for i in (-2, -1, 0, 1, 2):
        for j in (-2, -1, 0, 1, 2):
            y_start = y_center - i*block_size
            x_start = x_center - j*block_size
            # Create the window
            window = x[y_start:y_start+block_size, x_start:x_start+block_size]
            # Multiply it by the hamming window
            window = window * hw
            # Compute squared DFT magnitude of window
            window = (1/block_size**2)*np.abs(np.fft.fft2(window))**2
            window = np.fft.fftshift(window)
            total_pwr_spec_density += window / 25
            # windows.append(window)
    return total_pwr_spec_density


# Read in a gray scale TIFF image.
im = Image.open('img04g.tif')
print('Read img04.tif.')
print('Image size: ', im.size)

# Display image object by PIL.
im.show(title='image')

# Import Image Data into Numpy array.
# The matrix x contains a 2-D array of 8-bit gray scale values. 
x = np.array(im)
print('Data type: ', x.dtype)

# Display numpy array by matplotlib.
plt.imshow(x, cmap=plt.cm.gray)
plt.title('Image')

# Set colorbar location. [left, bottom, width, height].
cax =plt.axes([0.9, 0.15, 0.04, 0.7]) 
plt.colorbar(cax=cax)
plt.show()

x = np.double(x)/255.0

i = 99
j = 99
N = 256

z = x[i:N+i, j:N+j]

# Compute the power spectrum for the NxN region.
Z = (1/N**2)*np.abs(np.fft.fft2(z))**2

# Use fftshift to move the zero frequencies to the center of the plot.
Z = np.fft.fftshift(Z)

# Compute the logarithm of the Power Spectrum.
Zabs = np.log(Z)

# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = N)
X, Y = np.meshgrid(a, b)

surf = ax.plot_surface(X, Y, Zabs, cmap=plt.cm.coolwarm)

ax.set_xlabel('$\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')
ax.set_title(f"{N}x{N} Power Spectral Density")

fig.colorbar(surf, shrink=0.5, aspect=5)

fig.savefig(f"images/log-pwr-spec-density-{N}x{N}.png")

plt.show()

# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
N = 64
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = N)
X, Y = np.meshgrid(a, b)

surf = ax.plot_surface(X, Y, np.log(BetterSpecAnal(x)), cmap=plt.cm.coolwarm)

ax.set_xlabel('$\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')
ax.set_title(f"Better Power Spectral Density")

fig.colorbar(surf, shrink=0.5, aspect=5)

fig.savefig(f"images/log-pwr-spec-density-better.png")

plt.show()