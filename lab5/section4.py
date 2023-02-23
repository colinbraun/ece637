import matplotlib.pyplot as plt
import numpy as np
from training_data.read_data import read_data, display_samples

X = read_data()
u = np.mean(X, axis=1)
n = X.shape[1]
for col in range(X.shape[1]):
    X[:, col] -= u
# X = X / np.sqrt(n)

# Find the Eigenvalues and Eigenvectors of the image covariance for this data set
Z = X / np.sqrt(n)
U, S, Vh = np.linalg.svd(Z)
eigvecs = U
eigvals = S**2

fig, axs = plt.subplots(3, 4)
for k in range(12):
    img = np.reshape(eigvecs[:, k], (64, 64))

    axs[k//4,k%4].imshow(img, cmap=plt.cm.gray, interpolation='none') 
    # axs[k//4,k%4].set_title([k])
plt.savefig('eigenimages.png')
# plt.show()
plt.clf()


Y = U[:, 0:10].T @ X
# plt.figure()
x = [i for i in range(1, 11)]
plt.plot(x, Y[0:10, 0])
plt.plot(x, Y[0:10, 1])
plt.plot(x, Y[0:10, 2])
plt.plot(x, Y[0:10, 3])
plt.legend(["a", "b", "c", "d"])
plt.savefig("projection-coefficients")
plt.clf()
# plt.show()

fig, axs = plt.subplots(3, 2)
for i, m in enumerate([1, 5, 10, 15, 20, 30]):
    Y = U[:, 0:m].T @ X
    X_hat = U[:, 0:m] @ Y
    axs[i//2, i%2].imshow((X_hat[:, 0] + u).reshape(64, 64), cmap=plt.cm.gray, interpolation='none')
    axs[i//2, i%2].set_title(f"m = {m}")
plt.savefig("resynthesized-images.png")
# plt.show()
plt.clf()
# plt.imshow(X[:, 0].reshape(64, 64))
plt.imshow((X[:, 0] + u).reshape(64, 64), cmap=plt.cm.gray, interpolation='none')
plt.savefig("original-image.png")
# plt.show()
plt.clf()