import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm

def display_stripes(g):
    """
    Display stripes of gray and checkerboard.

    g: the gray level
    """
    gray = cm.get_cmap('gray', 256)
    checker_row = np.zeros([4, 256])
    for row in range(4):
        for col in range(256):
            if row == 0 or row == 1:
                if col % 4 < 2:
                    checker_row[row, col] = 255
            else:
                if col % 4 >= 2:
                    checker_row[row, col] = 255
    # The image is periodic along the rows. Create a single period.
    period = np.ones([32, 256]) * g
    # Add the checkerboard pattern to the period
    for i in range(4):
        period[i*4:(i+1)*4] = checker_row

    striped = np.tile(period, (8, 1))
    plt.imshow(striped, cmap=gray)
    # plt.show()

# -------------SECTION 4.2----------------
display_stripes(140)
plt.savefig("matching-gray-levels-140.png")


# -------------SECTION 4.3----------------
gray = cm.get_cmap('gray', 256)
im = Image.open('linear.tif')
x = np.array(im)
gamma = 1.156
x = x**(1/gamma)
plt.imshow(x, cmap=gray)
plt.savefig("linear-gamma-corrected.png")
plt.clf()
# plt.show()

# -------------SECTION 4.4----------------
im = Image.open('gamma15.tif')
x = np.array(im)
x = (x**1.5)**(1/gamma)
plt.imshow(x, cmap=gray)
plt.savefig("gamma15-gamma-corrected.png")
