from instapy.python_filters import python_color2gray, python_color2sepia

import numpy as np
from PIL import Image
import numpy.testing as nt

def test_color2gray(image):
    # ---------- sanity tests -------------
    actual_gray = python_color2gray(image)
    assert actual_gray.shape == image.shape
    assert actual_gray.dtype == "uint8"
    # test for uniform values
    nt.assert_allclose(actual_gray[:,:,0],actual_gray[:,:,1])
    nt.assert_allclose(actual_gray[:,:,1],actual_gray[:,:,2])


    gray_transform = np.array([0.21, 0.72, 0.07])

    test_pixels = [[0,0],[10,10],[100,100],[150,150]]

    for pixel in test_pixels:
        img_rgb = image[pixel[0]][pixel[1]]
        true_rgb = (gray_transform @ img_rgb).astype("uint8")

        calculated_rgb = actual_gray[pixel[0]][pixel[1]].astype("uint8")
        nt.assert_allclose(calculated_rgb,true_rgb)

    # ------------ test with premade ----------------
    premade_image = np.asarray(Image.open("testimg.jpg"))
    # this image has been checked by hand to see that it has
    # the correct rgb values according to the transformation
    # in the assignment
    # we use png here because of jpeg compression
    premade_gray = np.asarray(Image.open("refgray.png"))
    actual_gray_premade = python_color2gray(premade_gray)

    # we use 1 because every error i have found is that one of the implementations
    # has a value one more or one less than the other. This is probably floating
    # point stuff from the conversion from floats to uint8
    # ignore the last layer in premade_gray, because it is the transparancy
    # layer in a png
    nt.assert_allclose(actual_gray_premade,premade_gray[:,:,0:3], atol=1)


def test_color2sepia(image):
    # ---------- sanity tests -------------
    sepia_matrix = np.array([
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ])

    actual_sepia = python_color2sepia(image)


    # testing some random pixels
    test_pixels = [[0,0],[10,10],[100,100],[150,150]]

    for pixel in test_pixels:
        img_rgb = image[pixel[0]][pixel[1]]
        print(img_rgb.shape)
        true_rgb = sepia_matrix @ img_rgb
        # we must deal with overflows
        highest = np.max(true_rgb)
        if highest > 255:
            ratio = 255/highest
            true_rgb *= ratio

        true_rgb = true_rgb.astype("uint8")

        calculated_rgb = actual_sepia[pixel[0]][pixel[1]]
        nt.assert_allclose(calculated_rgb,true_rgb,atol=1)

    assert actual_sepia.shape == image.shape

    # --------- testing with premade ---------------
    premade_image = np.asarray(Image.open("testimg.jpg"))
    # this image has been checked by hand to see that it has
    # the correct rgb values according to the transformation
    # in the assignment
    premade_sepia = np.asarray(Image.open("refsepia.png"))

    actual_sepia_premade = python_color2sepia(premade_image)


    # ignore the last layer in premade_sepia, because it is the transparancy
    # layer in a png
    nt.assert_allclose(actual_sepia_premade, premade_sepia[:,:,0:3], atol=1)
