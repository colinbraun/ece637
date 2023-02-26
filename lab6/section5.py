from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

inc = 0.005
x_t = np.arange(0, 1+inc, inc)
y_t = np.arange(0, 1+inc, inc)
x, y = np.meshgrid(x_t, y_t)
z = np.ones(x.shape) - x - y
R709 = np.array([0.64, 0.330, 0.030])
G709 = np.array([0.300, 0.600, 0.100])
B709 = np.array([0.150, 0.060, 0.790])
mat = np.array([R709, G709, B709]).T
# M transforms from (r, g, b) to (X, Y, Z)
M = mat @ np.diag([1, 1, 1])
# Minv goes the other direction
Minv = np.linalg.inv(M)

image = np.zeros((x.shape[0], x.shape[1], 3))

# Take each pixel in XYZ array to RGB coordinates
for row in range(x.shape[0]):
    for col in range(x.shape[1]):
        image[row, col] = (Minv @ np.array([x[row, col], y[row, col], z[row, col]]).reshape(3, 1)).flatten()
        if image[row, col, 0] < 0 or image[row, col, 1] < 0 or image[row, col, 2] < 0:
            image[row, col, 0] = 1
            image[row, col, 1] = 1
            image[row, col, 2] = 1

gamma = 2.2
image = image**(1/gamma)
plt.imshow(image, extent=[0, 1, 0, 1])

# Load data.npy
data = np.load('data.npy', allow_pickle=True)[()]

# Create data from 400 to 700, separated by 10 each
wavelengths = np.arange(400, 710, 10)

x = data['x']
y = data['y']
z = data['z']
sums = [x[0, i]+y[0, i]+z[0, i] for i in range(len(x.flatten()))]
X = np.divide(x, sums)
Y = np.divide(y, sums)
Z = np.divide(z, sums)
# Add first point to end for closed loop when plotting
X = np.append(X, X[0])
Y = np.append(Y, Y[0])
Z = np.append(Z, Z[0])

plt.plot(X.flatten(), Y.flatten())
plt.savefig('5-outlined-chromaticity-plot.png')
# plt.show()
plt.clf()