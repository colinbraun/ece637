from PIL import Image
import numpy as np
from scipy.signal import convolve2d
from tabulate import tabulate

def bmatrix(a):
    """Returns a LaTeX bmatrix

    :a: numpy array
    :returns: LaTeX bmatrix as a string
    """
    if len(a.shape) > 2:
        raise ValueError('bmatrix can at most display two dimensions')
    lines = str(a).replace('[', '').replace(']', '').splitlines()
    rv = [r'\begin{bmatrix}']
    rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
    rv +=  [r'\end{bmatrix}']
    return '\n'.join(rv)

def bw_threshold(img, t):
    """
    Compute a black and white version of the given img (2d np array) given threshold t.
    Returns: 2D np array with values of 0 and 255 corresponding to black and white pixels.
    """
    return (img > t).astype(np.uint8) * 255

def rmse(f, b):
    """
    Compute the root-mean square error between the two images.
    """
    return np.sqrt(1/(f.shape[0]*f.shape[1]) * np.sum((f-b)**2))

def fidelity(f, b):
    f_tilde = transform(f)
    b_tilde = transform(b)
    # The formula is the same, just pass in f_tilde and b_tilde to rmse
    return rmse(f_tilde, b_tilde)

def transform(img):
    # Ungamma correct
    gamma = 2.2
    fl = 255 * (img/255)**gamma
    # Construct the filter we wish to apply
    h = np.zeros([7, 7])
    sigma_squared = 2
    for i in range(7):
        for j in range(7):
            h[i, j] = np.e**(-((i-3)**2 + (j-3)**2)/(2*sigma_squared))
    # Make it so that the sum of h adds to 1 (handles the C coefficient)
    h = h / np.sum(h)
    filtered_img = convolve2d(fl, h, mode='same', boundary='fill', fillvalue=0)
    return 255 * (filtered_img / 255)**(1/3)


input_img = np.array(Image.open('house.tif'))
gamma = 2.2
input_linear = 255 * (input_img/255)**gamma
I2 = np.array([[1, 2], [3, 0]])
# I2N=np.block([[4*IN + 1,4*IN + 2],[4*IN + 3,4*IN]])
I4=np.block([[4*I2 + 1,4*I2 + 2],[4*I2 + 3,4*I2]])
I8=np.block([[4*I4 + 1,4*I4 + 2],[4*I4 + 3,4*I4]])
# print(I2)
# print(I4)
# print(I8)
print(bmatrix(I2))
print(bmatrix(I4))
print(bmatrix(I8))
T2 = 255 * (I2 + 0.5) / (2**2)
T4 = 255 * (I4 + 0.5) / (4**2)
T8 = 255 * (I8 + 0.5) / (8**2)
b2 = np.zeros(input_linear.shape)
b4 = np.zeros(input_linear.shape)
b8 = np.zeros(input_linear.shape)
bs = [b2, b4, b8]
Ts = [T2, T4, T8]
for index, b in enumerate(bs):
    N = Ts[index].shape[0]
    for i in range(input_linear.shape[0]):
        for j in range(input_linear.shape[1]):
            b[i, j] = 255 if input_linear[i, j] > Ts[index][i%N, j%N] else 0

# TODO: Determine if error and fidelity should be relative to linear image or input image
img_out2 = Image.fromarray(b2.astype(np.uint8))
img_out2.save("4-b2x2.tif")
print(f"Error 2x2: {rmse(input_img, b2)}")
print(f"Fidelity 2x2: {fidelity(input_img, b2)}")

img_out4 = Image.fromarray(b4.astype(np.uint8))
img_out4.save("4-b4x4.tif")
print(f"Error 4x4: {rmse(input_img, b4)}")
print(f"Fidelity 4x4: {fidelity(input_img, b4)}")

img_out8 = Image.fromarray(b8.astype(np.uint8))
img_out8.save("4-b8x8.tif")
print(f"Error 8x8: {rmse(input_img, b8)}")
print(f"Fidelity 8x8: {fidelity(input_img, b8)}")
