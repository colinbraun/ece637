import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
from latex import bmatrix

gray = cm.get_cmap('gray', 256)
y = np.array(Image.open('img14g.tif'))
x = np.array(Image.open('img14sp.tif'))
print(x.shape)

sr = np.arange(20, y.shape[0], 20)
sc = np.arange(20, y.shape[1], 20)
num_rows = len(sr) * len(sc)
num_cols = 7*7
Z = np.zeros([num_rows, num_cols])
Y = np.zeros([num_rows, 1])

for i, row in enumerate(sr):
    for j, col in enumerate(sc):
        index = i * len(sc) + j
        Y[index] = y[row, col]
        Z[index] = x[row-3:row+4, col-3:col+4].flatten()

print(Z.shape)
print(Y.shape)

R_zz = Z.T @ Z / Y.shape[0]
r_zy = Z.T @ Y / Y.shape[0]
print(R_zz.shape)
print(r_zy.shape)

theta_star = np.linalg.inv(R_zz) @ r_zy
result = np.zeros(x.shape)

for row in range(x.shape[0]):
    for col in range(x.shape[1]):
        if row < 3 or col < 3 or row > x.shape[0] - 4 or col > x.shape[1] - 4:
            result[row, col] = 0
            continue
        z_s = x[row-3:row+4, col-3:col+4].flatten()
        # print(z_s)
        # print(z_s.shape)
        # print(theta_star.shape)
        result[row, col] = z_s @ theta_star

# print(np.amax(result))
result = np.clip(result, 0, 255)
imsave = Image.fromarray(result.astype(np.uint8))
# imsave.save('1-img14bl-restored.png')
imsave.save('1-img14sp-restored.png')
print(bmatrix(np.round(theta_star, 3).reshape([7, 7])))
# print(str(np.round(theta_star, 4).reshape([7, 7])))
