import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm

def stretch(image, t1, t2):
    """
    Stretch out the histogram of pixel values in the range [t1, t2].
    Returns the transformed image.
    """
    flat = image.flatten()
    # Map the values below and above t2 to 0 and 255 respectively
    for i in range(len(flat)):
        if flat[i] <= t1:
            flat[i] = 0
        elif flat[i] >= t2:
            flat[i] = 255
        else:
            # Remap values ~t1 -> 0, ~t2 -> 255
            flat[i] = 255 / (t2-t1) * (flat[i] - t1)

    return flat.reshape(image.shape)
    

gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)
plt.hist(x.flatten(), bins=np.linspace(0,255,256))
# plt.show()
plt.clf()

stretched = stretch(x, 70, 180)
plt.imshow(stretched, cmap=gray)
plt.savefig("kids-stretched.png")
# plt.show()
plt.clf()

plt.hist(stretched.flatten(), bins=np.linspace(0,255,256))
plt.savefig("kids-stretched-histogram.png")
# plt.show()