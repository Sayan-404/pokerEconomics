from setuptools import setup, Extension
import os

# Get the absolute path to the build directory
base_dir = os.path.dirname(os.path.abspath(__file__))
libpheval_path = os.path.join(base_dir, 'build', 'libpheval.so.0.6.0')

module = Extension(
    'potential',
    sources=['simplified_hand_potential.c'],
    include_dirs=['include'],  # Add include directory
    # Add directory where libpheval.so.0.6.0 is located
    library_dirs=[libpheval_path],
    libraries=['pheval'],  # Link against libpheval
    extra_compile_args=['-fPIC'],  # Add extra compile arguments
    extra_link_args=['-shared'],  # Ensure shared object file is created
)

setup(
    name='potential',
    version='1.0',
    description='Python wrapper for poker potential calculation',
    ext_modules=[module]
)
