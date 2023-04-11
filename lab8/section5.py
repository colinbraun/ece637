from PIL import Image
import numpy as np
from scipy.signal import convolve2d

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

def in_bounds(i, j, arr2d):
    """
    Return True if i, j is in the bounds of the 2d array.
    """
    num_rows = len(arr2d)
    num_cols = len(arr2d[0])
    if i < num_rows and j < num_cols:
        return True
    else:
        return False

input_img = np.array(Image.open('house.tif'))
gamma = 2.2
input_linear = 255 * (input_img/255)**gamma
output = np.zeros(input_img.shape)

T = 127
weights = [7/16, 3/15, 5/16, 1/16]
for i in range(output.shape[0]):
    for j in range(output.shape[1]):
        future_pixels = ((i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1))
        output[i, j] = int(input_linear[i, j] > 127) * 255
        error = input_linear[i, j] - output[i, j]
        for index, pixel_coords in enumerate(future_pixels):
            # print(pixel_coords)
            if in_bounds(*pixel_coords, output):
                input_linear[pixel_coords] += error * weights[index]

input_linear_original = 255 * (input_img/255)**gamma
result = Image.fromarray(output.astype(np.uint8))
result.save("5-diffusion-result.png")
print(f"Error 4x4: {rmse(input_linear_original, output)}")
print(f"Fidelity: {fidelity(input_linear_original, output)}")