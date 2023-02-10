import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm

def equalize(x):
    """
    Equalize the image x using histogram equalization. x is left untouched.

    Returns: A histogram-equalized version of x
    """
    fx = cdf(x)
    flat_x = x.flatten()
    y = np.zeros(flat_x.shape)
    for i, pixel_val in enumerate(flat_x):
        y[i] = fx[pixel_val]
    y_min = np.amin(y)
    y_max = np.amax(y)
    z = 255 * (y - y_min) / (y_max - y_min)
    return z.reshape(x.shape)

def cdf(x):
    """
    Compute and return the cummulative distribution function of the image x.
    """
    fx = np.zeros([256])
    # The below does not work well
    # histogram, _ = np.histogram(x.flatten(), bins=256)
    histogram = np.zeros([256])
    for pixel_val in x.flatten():
        histogram[pixel_val] += 1
    # print(histogram)
    # print(sum(histogram[0]))
    total = np.sum(histogram)
    for i in range(len(fx)):
        fx[i] = np.sum(histogram[0:i+1]) / total
    return fx

gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)

fx = cdf(x)
plt.plot(np.linspace(0, 255, 256), fx)
plt.savefig("kids-fx.png")
plt.clf()
equalized = equalize(x)
plt.hist(equalized.flatten(), bins=np.linspace(0,255,256))
plt.savefig("kids-equalized-histogram.png")
plt.clf()
plt.imshow(equalized, cmap=gray)
plt.savefig("kids-equalized-image.png")

# plt.imshow(x, cmap=gray)
