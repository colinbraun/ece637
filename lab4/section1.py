import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm



gray = cm.get_cmap('gray', 256)
im = Image.open('race.tif')
x = np.array(im)
# plt.imshow(x, cmap=gray)
plt.hist(x.flatten(), bins=np.linspace(0,255,256))
plt.savefig("race-histogram.png")

plt.clf()
im = Image.open('kids.tif')
x = np.array(im)
# plt.imshow(x, cmap=gray)
plt.hist(x.flatten(), bins=np.linspace(0,255,256))
plt.savefig("kids-histogram.png")
