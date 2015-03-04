# -*- coding: utf-8 -*-
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='keggrest',
      version='0.1.2',
      description='Basic frontend for the kegg database rest API',
      author='Enrico Giampieri',
      author_email='enrico.giampieri@unibo.it',
      packages=['keggrest'],
      download_url='https://github.com/EnricoGiampieri/keggrest.git',
      url='https://github.com/EnricoGiampieri/keggrest.git',
      license = "BSD",
      long_description=read('README.md'),
      keywords = ["rest", "API", "bioinformatics", "kegg"],
      classifiers=[
          "License :: OSI Approved :: BSD License",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Science/Research",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
          ],
      )