#!/bin/python3
# Template file for ece 637 labs
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from PIL import Image
from SpecAnal import BetterSpecAnal

def filter(x):
    """
    Filter the image x with a particular filter for problem 2.2
    """
    result = np.zeros([len(x), len(x[0])])
    # result[0, 0] = x[0, 0]
    
    for row in range(len(x)):
        for col in range(len(x[row])):
            t1 = x[row][col]
            if row-1 < 0:
                t2 = 0
            else:
                t2 = 0.99 * result[row-1][col]
            if col-1 < 0:
                t3 = 0
            else:
                t3 = 0.99 * result[row][col-1]
            if row-1 < 0 or col-1 < 0:
                t4 = 0
            else:
                t4 = -0.9801 * result[row-1][col-1]
            
            result[row][col] = t1 + t2 + t3 + t4
                
    return result

def h(u, v):
    """
    Compute the transfer function of the IIR filter at the specified spatial frequency domain points.
    """
    values = 3 / (1 - 0.99*np.exp(-1j*u) - 0.99*np.exp(-1j*v) + 0.9801*np.exp(-1j*u)*np.exp(-1j*v))
    return np.absolute(values)**2

x = np.random.uniform(-0.5, 0.5, [512, 512])
x_scaled = 255 * (x + 0.5)
plt.imshow(x_scaled.astype(np.uint8), cmap=plt.cm.binary)
print(x_scaled.dtype)
plt.savefig("images/np-rand-uniform.png")
# plt.show()
plt.clf()
y = filter(x) + 127
plt.imshow(y.astype(np.uint8), cmap=plt.cm.binary)
# print(filter(x) + 127)
plt.savefig("images/image-p-127.png")
# plt.show()
plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = 64)
X, Y = np.meshgrid(a, b)

Z = np.log((BetterSpecAnal(y)))

surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm)

plt.savefig("images/y-log-pwr-spec-density-better.png")

figure = plt.figure()
axis = figure.add_subplot(111, projection='3d')

u = np.linspace(-pi, pi, 1000)
v = np.linspace(-pi, pi, 1000)
U, V = np.meshgrid(u, v)
# ----------------SECTION 3 PLOTTING-----------------
z = np.array(h(U.ravel(), V.ravel()))
Z = z.reshape(U.shape)

axis.plot_surface(U, V, np.log(Z), cmap=plt.cm.coolwarm)
# axis.set_zlim(-2.5, 10)
plt.savefig("images/y-log-pwr-spec-density-theoretical.png")
# plt.show()
