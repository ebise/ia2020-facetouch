#!/usr/bin/env python

from setuptools import setup,find_packages

setup(name='src',
      version='0.0.1',
      author="FaceTouch",
      description="A auxiliary package for data preprocessing and visualization",
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.6.9',
      )