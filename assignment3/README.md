# Instapy

Instapy is a python package which can be used to filter images using grayscale or
sepia filters. The package allows you to choose your desired implementation (pure python,
numpy or numba), and see the different runtimes. It is also possible to decide how much
sepia filter you would like to apply using the optional ```k``` parameter.

## Installation

Clone this repo and run ``` $ pip install .```.

## Usage

You can either import your desired module (ex. ```from instapy.numpy_filters import *```)
in a python script or run the package from the command line with ```$ instapy FILE```.
There are many optional arguments for this CLI, they can be displayed by running
``` $ instapy --help```. 
