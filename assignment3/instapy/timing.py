"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
from . import io
from typing import Callable, Tuple
import numpy as np
from PIL import Image


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> Tuple[float, np.ndarray]:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    total = 0
    for i in range(calls):
        start = time.time()
        output = filter_function(*arguments)
        total += (time.time() - start)
    return total/calls, output


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    filter_names = ["color2gray", "color2sepia"]
    implementations = ["numpy", "numba"]

    # load the image
    image = Image.open(filename)
    pixels = np.asarray(image)
    # print the image name, width, height
    print(f"Timing performed using {filename}: {pixels.shape[0]}x{pixels.shape[1]}")
    # iterate through the filters
    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = instapy.get_filter(filter_name, "python")
        # time the reference implementation
        reference_time, _ = time_one(reference_filter,pixels)
        print(
            f"\nReference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        for implementation in implementations:
            filter = instapy.get_filter(filter_name, implementation)
            # time the filter
            filter_time, _ = time_one(filter,pixels)
            # compare the reference time to the optimized time
            speedup = reference_time/filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
