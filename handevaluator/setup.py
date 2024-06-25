from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'phevaluator_bindings',
        sources=['bindings.cpp'],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True),
            './include'
            ],
        extra_compile_args=['-std=c++11'],  # Add this line
    ),
]

setup(
    name='phevaluator_bindings',
    ext_modules=ext_modules,
)
