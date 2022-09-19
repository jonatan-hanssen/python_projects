"""pure Python implementation of image filters"""

import numpy as np
from typing import Optional


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


def python_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image,dtype="float16")
    m, n, p = image.shape

    if not 0 <= k <= 1:
        raise ValueError("k must be between [0-1], got {k=}")

    # what does "tuning" sepia mean? I dont know anything about the sepia filter
    # so I dont know if it makes any sense to have k linearly turn the sepia matrix
    # into the identity matrix or not. Maybe it should exponentially do it or
    # maybe the values should move by some polynomial between idenitity and sepia.
    # Regardless, this seems to work: linearly move the sepia matrix to the identity
    # matrix as a function of k
    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    scaling_matrix = [
        [ 0.607, -0.769, -0.189],
        [ -0.349, 0.314, -0.168],
        [ -0.272, -0.534, 0.869],
    ]

    # assume that k should scale the values linearly, simply add the scaling matrix
    for i in range(3):
        for j in range(3):
            sepia_matrix[i][j] += scaling_matrix[i][j]*(1-k)

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
