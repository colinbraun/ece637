import numpy as np
import matplotlib.pyplot as plt

# ---------------------SECTION 2.1---------------------
n = 1000
W = np.random.normal(0, 1, (2, n))
Rx = np.array([[2, -1.2], [-1.2, 1]])
evals, evecs = np.linalg.eig(Rx)
evals = np.diag(evals)
X_tilde = np.dot(np.sqrt(evals), W)
print(X_tilde.shape)
print(evecs.shape)
X = np.dot(evecs, X_tilde)
# print(w)
plt.figure()
plt.scatter(W[0, :], W[1, :])
plt.axis('equal')
# plt.show()
plt.clf()

plt.figure()
plt.scatter(X_tilde[0, :], X_tilde[1, :])
plt.axis('equal')
# plt.show()
plt.clf()

plt.figure()
plt.scatter(X[0, :], X[1, :])
plt.axis('equal')
# plt.show()
plt.clf()
# ---------------------SECTION 2.2---------------------
u = np.mean(X, 1)
Z = np.copy(X)
for col in range(Z.shape[1]):
    Z[:, col] -= u
R_hat = 1/(n-1) * np.dot(Z, np.transpose(Z))
print(R_hat)
