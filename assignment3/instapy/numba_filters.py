"""numba-optimized filters"""
from numba import jit
import numpy as np


@jit
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform

    pixels = np.asarray(image)
    gray_image = np.empty_like(image)

    m, n, p = pixels.shape
    gray_transform = [0.21, 0.72, 0.07]

    for i in range(m):
        for j in range(n):
            for k in range(p):
                gray_image[i][j][k] = pixels[i][j][k]*gray_transform[k]

    return gray_image.astype("uint8")


def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    ...

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image


...
