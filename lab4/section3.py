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
            # 
            # Suppose t1 = 10, t2 = 240, flat[i] = 11 -> ~0
            # Suppose t1 = 10, t2 = 240, flat[i] = 239 -> ~255
            flat[i] = (t2-t1) * flat[i] - t1
    
    