from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from latex import bmatrix
# Load data.npy
data = np.load('data.npy', allow_pickle=True)[()]
reflect = np.load('reflect.npy', allow_pickle=True)[()]
R = reflect['R']
I = np.zeros(R.shape)

# Create data from 400 to 700, separated by 10 each
wavelengths = np.arange(400, 710, 10)

x = data['x']
y = data['y']
z = data['z']
cmf = [x, y, z]
sums = [x[0, i]+y[0, i]+z[0, i] for i in range(len(x.flatten()))]
X = np.divide(x, sums)
Y = np.divide(y, sums)
Z = np.divide(z, sums)
illum1 = data['illum1']
illum2 = data['illum2']

for i in range(R.shape[2]):
    I[:, :, i] = illum2[0, i] * R[:, :, i]

XYZ = np.zeros((R.shape[0], R.shape[1], 3))

# Iterate over X, Y, and Z (the tristimulus values we are about to compute)
for i in range(XYZ.shape[2]):
    # Iterate over the wavelengths
    for j in range(R.shape[2]):
        XYZ[:, :, i] += cmf[i][0, j] * I[:, :, j]

# The white D_{65} white point
d65_wp = np.array([0.3127, 0.3290, 0.3583])
# The Rec. 709 RGB primaries
R709 = np.array([0.64, 0.330, 0.030])
G709 = np.array([0.300, 0.600, 0.100])
B709 = np.array([0.150, 0.060, 0.790])
mat = np.array([R709, G709, B709]).T
k = np.linalg.inv(mat) @ np.array([d65_wp[0]/d65_wp[1], 1, d65_wp[2]/d65_wp[1]]).reshape((3, 1))
# M transforms from (r, g, b) to (X, Y, Z)
M = mat @ np.diag(k.flatten())
# Minv goes the other direction
Minv = np.linalg.inv(M)
print(Minv)
print(bmatrix(Minv))

RGB = np.zeros(XYZ.shape)

# Take each pixel in XYZ array to RGB coordinates
for row in range(XYZ.shape[0]):
    for col in range(XYZ.shape[1]):
        RGB[row, col] += (Minv @ XYZ[row, col].reshape((3, 1))).flatten()

# Clip values to be between 0 and 1
RGB = np.clip(RGB, 0, 1)

# Perform gamma correction
gamma = 2.2
# gamma = 1
RGB = RGB**(1/gamma)
# Scale to be in range 0 to 255
RGB = RGB * 255

im = Image.fromarray(RGB.astype(np.uint8))
im.save("4-d65-illum2.png")
# image = Image.open('img.tif')
# x = np.array(im)
