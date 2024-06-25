# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("hand_potential.pyx"),
    include_dirs=[numpy.get_include()]
)