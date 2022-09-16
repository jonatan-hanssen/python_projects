"""pure Python implementation of image filters"""

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)

    m, n, p = image.shape
    gray_transform = [0.21, 0.72, 0.07]

    for i in range(m):
        for j in range(n):
            for k in range(p):
                gray_image[i][j][k] = image[i][j][k]*gray_transform[k]

    # iterate through the pixels, and apply the grayscale transform

    # return pixels
    return gray_image.astype("uint8")


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image,dtype="float16")
    m, n, p = image.shape

    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    for i in range(m):
        for j in range(n):
            for k in range(p):
                sepia_image[i][j][k] = image[i][j][0]*sepia_matrix[k][0]
                sepia_image[i][j][k] += image[i][j][1]*sepia_matrix[k][1]
                sepia_image[i][j][k] += image[i][j][2]*sepia_matrix[k][2]
            # fix overflows
            highest = max(sepia_image[i][j])
            if highest > 255:
                ratio = 255/highest
                sepia_image[i][j][0] *= ratio
                sepia_image[i][j][1] *= ratio
                sepia_image[i][j][2] *= ratio

    return sepia_image.astype("uint8")
