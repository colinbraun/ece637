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
plt.savefig('w-2-1.png')
# plt.show()
plt.clf()

plt.figure()
plt.scatter(X_tilde[0, :], X_tilde[1, :])
plt.axis('equal')
plt.savefig('x-tilde-2-1.png')
# plt.show()
plt.clf()

plt.figure()
plt.scatter(X[0, :], X[1, :])
plt.axis('equal')
plt.savefig('x-2-1.png')
# plt.show()
plt.clf()

# ---------------------SECTION 2.2---------------------
u = np.mean(X, axis=1)
Z = np.copy(X)
for col in range(Z.shape[1]):
    Z[:, col] -= u
R_hat = 1/(n-1) * Z @ Z.T
print(R_hat)
evals, evecs = np.linalg.eig(R_hat)
evals_n12 = np.diag(1 / np.sqrt(evals))


X_tilde = evecs.T @ Z
# Switch with covariance mat (R_hat?) Double check in general
W = evals_n12 @ X_tilde
# W = R_hat @ X_tilde
uW = np.mean(W, axis=1)
Zw = np.copy(W)
for col in range(Zw.shape[1]):
    Zw[:, col] -= uW
R_hat_w = 1/(n-1) * Zw @ Zw.T
print(R_hat_w)


plt.figure()
plt.scatter(X_tilde[0, :], X_tilde[1, :])
plt.axis('equal')
plt.savefig('x-tilde-2-2.png')
# plt.show()
plt.clf()

plt.figure()
plt.scatter(W[0, :], W[1, :])
plt.axis('equal')
plt.savefig('w-2-2.png')
# plt.show()
plt.clf()
