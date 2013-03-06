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
      version='0.1',
      description='Basic frontend for the kegg database rest API',
      author='Enrico Giampieri',
      author_email='enrico.giampieri@unibo.it',
      py_modules=['keggrest'],
      download_url='https://github.com/EnricoGiampieri/keggrest.git',
      url='https://github.com/EnricoGiampieri/keggrest.git',
      license = "BSD",
      long_description=read('README.txt'),
      keywords = "rest API bioinformatics",
      classifiers=[
          "Development Status :: 0.1",
          "Topic :: Utilities",
          "License :: OSI Approved :: BSD License",
          ],
      )