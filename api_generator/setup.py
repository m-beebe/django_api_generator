from setuptools import setup, find_packages
from .src import __version__

setup(
    name='django_api_generator',
    version=__version__,
    packages=find_packages(exclude=[]),
    url='',
    license='',
    author='Bobeegan',
    author_email='',
    py_modules=['api_generator'],
    description='',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],
)
