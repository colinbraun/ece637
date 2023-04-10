from PIL import Image
import numpy as np

def bw_threshold(img, t):
    """
    Compute a black and white version of the given img (2d np array) given threshold t.
    Returns: 2D np array with values of 0 and 255 corresponding to black and white pixels.
    """
    return (img > t).astype(np.uint8) * 255

def rsme(img1, img2):
    """
    Compute the root-mean square error between the two images.
    """
    return np.sqrt(1/(img1.shape[0]*img1.shape[1]) * (img1-img2)**2)

input_img = np.array(Image.open('house.tif'))

# print(result)
# img_out = Image.fromarray(x)
# img_out.save('img_out.tif')
