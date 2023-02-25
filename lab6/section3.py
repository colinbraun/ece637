import matplotlib.pyplot as plt
import numpy as np
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
illum1 = data['illum1']
illum2 = data['illum2']

x_cie = [0.73467, 0.27376, 0.16658, 0.73467]
y_cie = [0.26533, 0.71741, 0.00886, 0.26533]
x_709 = [0.640, 0.300, 0.150, 0.640]
y_709 = [0.330, 0.600, 0.060, 0.330]
plt.plot(X.flatten(), Y.flatten())
plt.plot(x_cie, y_cie)
plt.plot(x_709, y_709)
labels_cie = [r"$R_{CIE\_1931}$", r"$G_{CIE\_1931}$", r"$B_{CIE\_1931}$"]
labels_709 = [r"$R_{709}$", r"$G_{709}$", r"$B_{709}$"]
for i in range(3):
    plt.text(x_cie[i], y_cie[i], labels_cie[i])
    plt.text(x_709[i], y_709[i], labels_709[i])

plt.scatter([0.3127], [0.3290])
plt.text(0.3127, 0.3290, r"$D_{65}$ Point")
plt.scatter([0.3333], [0.3333])
plt.text(0.3333, 0.3333, r"EE Point")
plt.savefig('3-chromaticities-pure-source.png')
# plt.show()
plt.clf()
