import matplotlib.pyplot as plt
import numpy as np
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
sums = [x[0, i]+y[0, i]+z[0, i] for i in range(len(x.flatten()))]
X = np.divide(x, sums)
Y = np.divide(y, sums)
Z = np.divide(z, sums)
illum1 = data['illum1']
illum2 = data['illum2']

for i in range(R.shape[2]):
    I[:, :, i] = illum1[i] * R[:, :, i]

XYZ = np.zeros((R.shape[0], R.shape[1], 3))
