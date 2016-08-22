#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name='makeatoss',
  version='0.0.1',
  description='project for makeatoss',
  author='Osamu Sugiyama',
  author_email='sugiyama@kuhp.kyoto-u.ac.jp',
  package_dir={'': 'src'},
  packages=find_packages('src'),
  install_requires=(
    'python-memcached',
  )
)
