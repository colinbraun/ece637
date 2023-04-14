from PIL import Image
import numpy as np
from scipy.signal import convolve2d

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
binary_img = bw_threshold(input_img, 127)
error = rmse(input_img, binary_img)
fid = fidelity(input_img, binary_img)

print(f"Error: {error}")
print(f"Fidelity: {fid}")
result = Image.fromarray(binary_img)
result.save("3-thresholded-image.tif")



# print(result)
# img_out = Image.fromarray(x)
# img_out.save('img_out.tif')
