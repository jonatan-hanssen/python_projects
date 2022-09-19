"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import io
from . import timing


def run_filter(
    file: str,
    *, # it seemed more reasonable to solve this with kwargs
    out_file: str = None,
    # we dont want the slowest implementation to be the default
    implementation: str = "numpy",
    # scale factor should be an float, not a int
    scale: float = 1,
    k: float = 1,
    runtime: bool = False,
    gray: bool = True,
    sepia: bool = False,
) -> None:

    """Run the selected filter"""
    if sepia:
        filter = "color2sepia"
    else:
        filter = "color2gray"

    # load the image from a file
    image = Image.open(file)
    if scale != 1:
        if scale <= 0:
            raise ValueError("Scale cannot be negative")
        # we probably do not want to allow arbitrary resizing, considering
        # how big the file can get
        if scale > 5:
            raise ValueError("Scale cannot be higher than 5")

        image = image.resize((int(image.width * scale), int(image.height * scale)))

    pixels = np.asarray(image)
    filter_func = instapy.get_filter(filter, implementation)

    if not runtime:
        if filter == "color2sepia" and k:
            filtered = filter_func(pixels, k)
        else:
            filtered = filter_func(pixels)
    else: 
        if filter == "color2sepia" and k:
            time, filtered = timing.time_one(filter_func, pixels, k)
        else:
            time, filtered = timing.time_one(filter_func, pixels)
        print(f"Average time over 3 runs: {time:.3}s using {implementation}")

    if out_file:
        io.write_image(filtered,out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Applies a grayscale or sepia filter on the given image")

    # you cannot have gray and sepia at the same time
    group = parser.add_mutually_exclusive_group()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")
    group.add_argument("-g", "--gray", 
            help="Select gray filter", 
            action="store_true")
    group.add_argument("-se", "--sepia", 
            help="Select sepia filter", 
            action="store_true")
    parser.add_argument("-r", "--runtime", 
            help="Track average runtime", 
            action="store_true")
    parser.add_argument("-sc", "--scale", 
            help="Scale factor to resize image", 
            type=float)
    parser.add_argument("-k", 
            help="Scale how much sepia should be applied. Accepts k between [0,1]", 
            type=float)
    parser.add_argument("-i", "--implementation", 
            help="Choose implementation", 
            choices=["python", "numpy", "numba"])

    # parse arguments and call run_filter
    args = parser.parse_args()

    # make keyword arguments
    argdict = vars(args)
    argdict = {key: value for key, value in argdict.items() if 
            value is not None and 
            value is not False}
    # this is a positional argument
    argdict.pop("file")

    run_filter(args.file, **argdict)
