from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy.testing as nt
import numpy as np
from PIL import Image


def test_color2gray(image, reference_gray):
    # ------------ test with reference ----------------
    actual_gray = numpy_color2gray(image)
    assert actual_gray.dtype == "uint8"
    assert actual_gray.shape == image.shape

    # we use 1 because every error i have found is that one of the implementations
    # has a value one more or one less than the other. This is probably floating
    # point stuff from the conversion from floats to uint8
    nt.assert_allclose(actual_gray,reference_gray, atol=1)

    # ------------ test with premade ----------------
    premade_image = np.asarray(Image.open("testimg.jpg"))
    # this image has been checked by hand to see that it has
    # the correct rgb values according to the transformation
    # in the assignment
    # we use png here because of jpeg compression
    premade_gray = np.asarray(Image.open("refgray.png"))
    actual_gray_premade = numpy_color2gray(premade_gray)

    # ignore the last layer in premade_gray, because it is the transparancy
    # layer in a png
    nt.assert_allclose(actual_gray_premade,premade_gray[:,:,0:3], atol=1)


def test_color2sepia(image, reference_sepia):
    # ------------ test with reference ----------------
    actual_sepia = numpy_color2sepia(image)
    assert actual_sepia.dtype == "uint8"
    assert actual_sepia.shape == image.shape

    nt.assert_allclose(actual_sepia, reference_sepia, atol=1)

    # ------------ test with premade ----------------
    premade_image = np.asarray(Image.open("testimg.jpg"))

    # this image has been checked by hand to see that it has
    # the correct rgb values according to the transformation
    # in the assignment
    premade_sepia = np.asarray(Image.open("refsepia.png"))
    actual_sepia_premade = numpy_color2sepia(premade_image)
    # ignore the last layer in premade_sepia, because it is the transparancy
    # layer in a png
    nt.assert_allclose(actual_sepia_premade, premade_sepia[:,:,0:3], atol=1)
