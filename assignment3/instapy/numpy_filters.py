"""numpy implementation of image filters"""

from typing import Optional
import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)

    gray_transform = np.array([0.21, 0.72, 0.07])

    gray_image = np.empty_like(image)

    # einsum works as follows: we say that gray_transform has an axis labeled k.
    # we then say that image has axises labeled ijk, and because we labeled the last
    # one k we tell numpy we want to multiply over this axis. We the label the output
    # array with ij, which says we want to sum over the axis k aswell. This
    # gives us the desired output.
    gray_image = np.einsum("k,ijk->ij",gray_transform, image)
    # However, we want to return an rgb image, which means 3 values for each x,y
    gray_image = np.dstack((gray_image,gray_image,gray_image))

    return gray_image.astype("uint8")


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """
    m, n, p = image.shape

    if not 0 <= k <= 1:
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.empty_like(image,dtype="float16")

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)


    # what does "tuning" sepia mean? I dont know anything about the sepia filter
    # so I dont know if it makes any sense to have k linearly turn the sepia matrix
    # into the identity matrix or not. Maybe it should exponentially do it or
    # maybe the values should move by some polynomial between idenitity and sepia.
    # Regardless, this seems to work: linearly move the sepia matrix to the identity
    # matrix as a function of k
    sepia_matrix = np.array([
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ])

    scaling_matrix = np.array([
        [ 0.607, -0.769, -0.189],
        [ -0.349, 0.314, -0.168],
        [ -0.272, -0.534, 0.869],
    ])

    # assume that k should scale the values linearly, simply add the scaling matrix
    sepia_matrix += scaling_matrix*(1-k)

    # it just works ladies and gentlemen
    sepia_image = np.einsum('ijk,lk->ijl',image, sepia_matrix)

    # fix overflows

    # find the highest value along the third axis (the rgb values)
    maxes = sepia_image.max(2) # this returns a M,N array

    overflows = np.where(maxes > 255, maxes, 255) # an array of 255 or higher values
    ratios = (np.ones((m,n))*255)/overflows # this is either one or something lower

    # this multiplies every pixel value with either one or the appropriate ratio in case
    # of overflows
    sepia_image *= np.dstack((ratios,ratios,ratios))

    return sepia_image.astype("uint8")
