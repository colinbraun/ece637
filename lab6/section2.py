import matplotlib.pyplot as plt
import numpy as np
# Load data.npy
data = np.load('data.npy', allow_pickle=True)[()]

# Create data from 400 to 700, separated by 10 each
wavelengths = np.arange(400, 710, 10)

x = data['x']
y = data['y']
z = data['z']
illum1 = data['illum1']
illum2 = data['illum2']
plt.plot(wavelengths, x.flatten())
plt.plot(wavelengths, y.flatten())
plt.plot(wavelengths, z.flatten())
plt.legend([r'$x_0$', r'$y_0$', r'$z_0$'])
plt.savefig('2-x0-y0-z0.png')
# plt.show()
plt.clf()

A_i = np.array([[0.2430, 0.8560, -0.0440], [-0.3910, 1.1650, 0.0870], [0.0100, -0.0080, 0.5630]])
xyz = np.array([x.flatten(), y.flatten(), z.flatten()])
lms = A_i @ xyz
l, m, s = lms[0, :], lms[1, :], lms[2, :]
plt.plot(wavelengths, l.flatten())
plt.plot(wavelengths, m.flatten())
plt.plot(wavelengths, s.flatten())
plt.legend([r'$l_0$', r'$m_0$', r'$s_0$'])
plt.savefig('2-l0-m0-s0')
# plt.show()
plt.clf()

plt.plot(wavelengths, illum1.flatten())
plt.plot(wavelengths, illum2.flatten())
plt.legend([r'$D_{65}$', 'Fluorescent'])
plt.savefig('2-d65-and-fluorescent-illuminants')
# plt.show()
plt.clf()

# plt.plot(wavelengths, l.flatten())
# plt.plot(wavelengths, s.flatten())
# plt.legend([r'$l_0$', r'$m_0$', r'$s_0$'])
# plt.savefig('2-l0-m0-s0')
# # plt.show()
# plt.clf()